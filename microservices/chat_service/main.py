from fastapi import FastAPI, HTTPException, Header, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import os
from openai import OpenAI
import httpx
from client import verify_key
import json
from prompt_builder import build_styled_prompt, format_user_context, DEFAULT_MN_PROMPT

openai_client = OpenAI()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://nginx:8080/api/auth")

async def verify_key(token: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{AUTH_SERVICE_URL}/verify", json={"key": token})
            return resp.status_code == 200 and resp.json().get("valid", False)
    except Exception as e:
        print("❌ Auth verification failed:", e)
        return False

# JWT authentication dependency
async def require_jwt(authorization: str | None = Header(None, alias="Authorization")):
    if os.getenv("ENV", "dev") == "dev":
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")
    token = authorization.split(" ", 1)[1]
    if not await verify_key(token):
        raise HTTPException(status_code=401, detail="Invalid token")

# Load root and service .env for unified configuration
root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=root_env, override=False)

service_env = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(dotenv_path=service_env, override=True)

ENV = os.getenv("ENV", "dev")
root_path = "/api/chat" if ENV == "prod" else ""

# Load environment
STORAGE_URL = os.getenv("STORAGE_URL", "http://localhost:8011")
RAG_URL = os.getenv("RAG_URL", "http://localhost:8017")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Import default prompt from prompt_builder
from prompt_builder import DEFAULT_MN_PROMPT as DEFAULT_PROMPT

app = FastAPI(
    title="Chat Service",
    description="Orchestrates chat turns by proxying to RAG, storage, auth & stats services",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"url": "openapi.json"},
    root_path=root_path,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "chat"}

class ChatRequest(BaseModel):
    """Payload for chat query including user context and MNTEST scores"""
    userId: str = Field(..., description="Cognito sub claim for the user")
    username: str = Field(..., description="User's unique username")
    fullName: Optional[str] = Field(None, description="User's display name")
    traitScores: Dict[str, float] = Field(
        ..., description="Map of 19 MNTEST trait names to their scores (1-10)"
    )
    message: str = Field(..., description="The user's current chat message")
    sessionId: str = Field(..., description="Identifier for this chat session")

    # ✅ Optional overrides from config panel
    systemPrompt: Optional[str] = Field(
        None, description="Custom system prompt to override default"
    )

    topK_RAG_hits: Optional[int] = Field(
        None, ge=1, le=10, description="How many RAG chunks to retrieve"
    )

class Document(BaseModel):
    """RAG source document returned to client"""
    text: str
    metadata: Dict[str, Any]

class ChatResponse(BaseModel):
    """Payload returned by /chat"""
    answer: str
    sources: List[Document]
    plan: Dict[str, Any]
    critique: str
    followup: str

class ErrorResponse(BaseModel):
    detail: str



# Endpoint to retrieve runtime configuration
@app.get("/config")
async def get_config():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config")
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch config from storage service: {e}")

@app.post(
    "/query",
    response_model=ChatResponse,
    responses={401: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
    tags=["chat"],
)
async def chat_endpoint(
    req: ChatRequest,
    authorization: str | None = Header(None, alias="Authorization"),
    _=Depends(require_jwt),
):
    # Stub response in dev mode to avoid real OpenAI calls
    if os.getenv("ENV", "dev") == "dev":
        return ChatResponse(answer="Dev stub response", sources=[], plan={}, critique="", followup="")
    # Extract token for downstream calls (empty in dev)
    token = authorization.split(" ", 1)[1] if authorization else ""

    # Prepare headers for internal service calls
    internal_headers = {"Authorization": authorization} if authorization else {}

    async with httpx.AsyncClient() as client:
        # 1. Retrieve session memory (conversation log)
        mem_resp = await client.get(
            f"{STORAGE_URL}/api/memory/session-memory/{req.sessionId}",
            headers=internal_headers
        )
        conversation_log = mem_resp.json().get("exchanges", []) if mem_resp.status_code == 200 else []

        # Extract past exchanges (support both flat list or nested 'exchanges')
        exchanges = []
        if isinstance(conversation_log, dict) and "exchanges" in conversation_log:
            exchanges = conversation_log.get("exchanges", [])
        elif isinstance(conversation_log, list):
            exchanges = conversation_log

        # 1b. Retrieve existing session summary (if any)
        sum_resp = await client.get(
            f"{STORAGE_URL}/api/memory/all-summaries/{req.userId}",
            headers=internal_headers
        )

        if sum_resp.status_code == 200:
            summaries = sum_resp.json().get("summaries", [])
            # Join oldest → newest summaries, capped to ~3000 chars
            session_summary = ""
            summary_chars = 0
            for s in summaries:
                if summary_chars + len(s) > 3000:
                    break
                session_summary += s + "\n"
                summary_chars += len(s)
        else:
            session_summary = ""

        # 1c. Get config defaults from storage service
        try:
            config_resp = await client.get(
                f"{STORAGE_URL}/api/memory/runtime-config",
                headers=internal_headers
            )
            config_defaults = config_resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch runtime config: {e}")

        top_k = req.topK_RAG_hits or config_defaults.get("top_k_rag_hits", 5)
        base_prompt = req.systemPrompt or config_defaults.get("system_prompt", DEFAULT_PROMPT)
        prompt_style = config_defaults.get("prompt_style", "default")
        custom_style_modifier = config_defaults.get("custom_style_modifier", None)
        
        # Build styled system prompt
        SYSTEM_PROMPT = build_styled_prompt(base_prompt, prompt_style, custom_style_modifier)

        # Build recent history (# of exchanges depends on config)
        MAX_HISTORY_CHARS = 10000
        history = ""
        char_count = 0

        # Reverse loop to prioritize most recent turns
        for ex in reversed(exchanges):
            turn = ""
            if "user_prompt" in ex and "assistant_response" in ex:
                turn = f"User: {ex['user_prompt']}\nAssistant: {ex['assistant_response']}\n"
            elif ex.get("role") and ex.get("content"):
                turn = f"{ex['role'].capitalize()}: {ex['content']}\n"

            if char_count + len(turn) > MAX_HISTORY_CHARS:
                break

            history = turn + history  # prepend so history flows oldest → newest
            char_count += len(turn)

        # 2. Retrieve relevant glossary/context via Vector Search service
        vs_resp = await client.post(f"{RAG_URL}/search", json={"query": req.message, "top_k": top_k})
        if vs_resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch glossary chunks")
        chunks = vs_resp.json()

        # Build context string from chunks
        context = "\n\n".join([c.get("chunk", "") for c in chunks])

        # 3. Assemble GPT prompt
        # Build user profile section with trait scores
        profile_lines = [f"Name: {req.fullName or 'User'}", f"Username: {req.username}"]
        profile_lines.append("\nTrait Scores:")
        
        # Group traits by score range for better interpretation
        dominant_traits = []
        balanced_traits = []
        suppressed_traits = []
        
        for trait, score in req.traitScores.items():
            trait_entry = f"- {trait.replace('_', ' ').title()}: {score}/10"
            if score >= 7:
                dominant_traits.append((trait, score))
            elif score <= 3:
                suppressed_traits.append((trait, score))
            else:
                balanced_traits.append((trait, score))
            profile_lines.append(trait_entry)
        
        # Add trait analysis summary
        if dominant_traits:
            profile_lines.append(f"\nDominant Traits (strengths): {', '.join([t[0].replace('_', ' ').title() for t in dominant_traits])}")
        if suppressed_traits:
            profile_lines.append(f"Suppressed Traits (growth areas): {', '.join([t[0].replace('_', ' ').title() for t in suppressed_traits])}")
        
        profile_section = "\n".join(profile_lines)
        
        # Format user context using the utility function
        user_context = format_user_context(
            user_profile=profile_section,
            session_summary=session_summary,
            recent_history=history,
            rag_context=context
        )
        
        # Build the final user message
        final_prompt = f"{user_context}\n\nCURRENT QUESTION:\n{req.message}"

        # 4. Call OpenAI with improved prompting
        try:
            # Use config values for OpenAI parameters
            model = config_defaults.get("model", "gpt-3.5-turbo")
            temperature = config_defaults.get("temperature", 0.7)
            max_tokens = config_defaults.get("max_tokens", 1000)
            presence_penalty = config_defaults.get("presence_penalty", 0.1)
            frequency_penalty = config_defaults.get("frequency_penalty", 0.1)
            
            completion = openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": final_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty
            )
            answer = completion.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")

        # 5. Persist new exchange to memory service
        new_exchanges = exchanges.copy()
        new_exchanges.append({"user_prompt": req.message, "assistant_response": answer})
        save_payload = {"uuid": req.userId, "conversation_log": {"exchanges": new_exchanges}}
        # 5. Persist new exchange to memory service
        await client.post(
            f"{STORAGE_URL}/api/memory/session-memory",
            json=save_payload,
            headers=internal_headers
        )

        # 6. Build response sources from vector chunks
        sources = []
        for c in chunks:
            sources.append({
                "text": c.get("chunk", ""),
                "metadata": {
                    "title": c.get("title"),
                    "topic": c.get("topic"),
                    "score": c.get("score"),
                }
            })
        return ChatResponse(
            answer=answer,
            sources=sources,
            plan={},
            critique="",
            followup="",
        )
    
@app.get("/admin", response_class=HTMLResponse)
async def config_ui():
    # In production, config will be loaded via client-side fetch with auth token
    # For initial render, provide defaults
    cfg = {
        "system_prompt": "",
        "top_k_rag_hits": 5,
        "prompt_style": "default",
        "custom_style_modifier": "",
        "temperature": 0.7,
        "max_tokens": 1000,
        "presence_penalty": 0.1,
        "frequency_penalty": 0.1,
        "model": "gpt-3.5-turbo"
    }

    return f"""
    <html>
    <head>
        <title>Xavigate Admin Panel</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1000px; margin: 0 auto; padding: 2rem; background: #f5f5f5; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem; }}
            h1 {{ margin: 0; font-size: 2rem; }}
            .subtitle {{ opacity: 0.9; margin-top: 0.5rem; }}
            .card {{ background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 2rem; }}
            .card h2 {{ margin-top: 0; color: #333; border-bottom: 2px solid #eee; padding-bottom: 1rem; }}
            textarea {{ width: 100%; min-height: 200px; font-family: monospace; padding: 1rem; border: 1px solid #ddd; border-radius: 5px; resize: vertical; }}
            input, select {{ padding: 0.75rem; font-size: 1rem; border: 1px solid #ddd; border-radius: 5px; }}
            input[type="number"] {{ width: 120px; }}
            input[type="range"] {{ width: 300px; }}
            .range-container {{ display: flex; align-items: center; gap: 1rem; }}
            .range-value {{ font-weight: bold; min-width: 50px; }}
            select {{ width: 250px; }}
            button {{ padding: 0.75rem 2rem; font-size: 1rem; border: none; border-radius: 5px; cursor: pointer; margin-right: 1rem; }}
            button[value="save"] {{ background: #667eea; color: white; }}
            button[value="test"] {{ background: #48bb78; color: white; }}
            button:hover {{ opacity: 0.9; }}
            label {{ display: block; margin-top: 1.5rem; margin-bottom: 0.5rem; font-weight: 600; color: #444; }}
            .help-text {{ font-size: 0.875rem; color: #666; margin-top: 0.25rem; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
            @media (max-width: 768px) {{ .grid {{ grid-template-columns: 1fr; }} }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🧭 Xavigate Admin Panel</h1>
            <p class="subtitle">Configure AI behavior, prompting, and system parameters</p>
        </div>
        <form method="POST" action="/admin">
            <div class="card">
                <h2>Prompt Configuration</h2>
                <label for="system_prompt">System Prompt:</label>
                <p class="help-text">Define how Xavigate should behave and respond to users</p>
                <textarea name="system_prompt">{cfg.get("system_prompt", "")}</textarea>

                <label for="prompt_style">Conversation Style:</label>
                <p class="help-text">Choose how Xavigate should interact with users</p>
                <select name="prompt_style">
                    <option value="default" {"selected" if cfg.get("prompt_style", "default") == "default" else ""}>Default - Warm & Insightful</option>
                    <option value="empathetic" {"selected" if cfg.get("prompt_style") == "empathetic" else ""}>Empathetic - Emotional Support</option>
                    <option value="analytical" {"selected" if cfg.get("prompt_style") == "analytical" else ""}>Analytical - Data-Driven</option>
                    <option value="motivational" {"selected" if cfg.get("prompt_style") == "motivational" else ""}>Motivational - Action-Oriented</option>
                    <option value="socratic" {"selected" if cfg.get("prompt_style") == "socratic" else ""}>Socratic - Question-Based</option>
                    <option value="custom" {"selected" if cfg.get("prompt_style") == "custom" else ""}>Custom Style</option>
                </select>

                <label for="custom_style_modifier">Custom Style Instructions:</label>
                <p class="help-text">Define your own conversation style (only used when Custom is selected)</p>
                <textarea name="custom_style_modifier" rows="3">{cfg.get("custom_style_modifier", "")}</textarea>
            </div>

            <div class="card">
                <h2>AI Model Parameters</h2>
                <div class="grid">
                    <div>
                        <label for="model">Model:</label>
                        <p class="help-text">OpenAI model to use</p>
                        <select name="model">
                            <option value="gpt-3.5-turbo" {"selected" if cfg.get("model", "gpt-3.5-turbo") == "gpt-3.5-turbo" else ""}>GPT-3.5 Turbo (Fast)</option>
                            <option value="gpt-4" {"selected" if cfg.get("model") == "gpt-4" else ""}>GPT-4 (Advanced)</option>
                            <option value="gpt-4-turbo-preview" {"selected" if cfg.get("model") == "gpt-4-turbo-preview" else ""}>GPT-4 Turbo (Latest)</option>
                        </select>

                        <label for="temperature">Temperature: <span class="range-value" id="temp-value">{cfg.get("temperature", 0.7)}</span></label>
                        <p class="help-text">Controls randomness (0=focused, 1=creative)</p>
                        <div class="range-container">
                            <input type="range" name="temperature" value="{cfg.get("temperature", 0.7)}" min="0" max="1" step="0.1" 
                                   oninput="document.getElementById('temp-value').textContent = this.value">
                        </div>

                        <label for="max_tokens">Max Tokens:</label>
                        <p class="help-text">Maximum response length</p>
                        <input type="number" name="max_tokens" value="{cfg.get("max_tokens", 1000)}" min="100" max="4000" step="100"/>
                    </div>
                    <div>
                        <label for="presence_penalty">Presence Penalty: <span class="range-value" id="presence-value">{cfg.get("presence_penalty", 0.1)}</span></label>
                        <p class="help-text">Encourages new topics (-2 to 2)</p>
                        <div class="range-container">
                            <input type="range" name="presence_penalty" value="{cfg.get("presence_penalty", 0.1)}" min="-2" max="2" step="0.1"
                                   oninput="document.getElementById('presence-value').textContent = this.value">
                        </div>

                        <label for="frequency_penalty">Frequency Penalty: <span class="range-value" id="freq-value">{cfg.get("frequency_penalty", 0.1)}</span></label>
                        <p class="help-text">Reduces repetition (-2 to 2)</p>
                        <div class="range-container">
                            <input type="range" name="frequency_penalty" value="{cfg.get("frequency_penalty", 0.1)}" min="-2" max="2" step="0.1"
                                   oninput="document.getElementById('freq-value').textContent = this.value">
                        </div>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>Memory & Context Settings</h2>
                <div class="grid">
                    <div>
                        <label for="top_k">RAG Results (Top K):</label>
                        <p class="help-text">Number of knowledge base results to include</p>
                        <input type="number" name="top_k" value="{cfg.get("top_k_rag_hits", 5)}" min="1" max="20"/>
                    </div>
                    <div>
                        <label for="conversation_history_limit">Conversation History:</label>
                        <p class="help-text">Number of previous exchanges to include</p>
                        <input type="number" name="conversation_history_limit" value="{cfg.get("conversation_history_limit", 5)}" min="0" max="20"/>
                    </div>
                </div>
            </div>

            </div>

            <div class="card">
                <h2>Test Configuration</h2>
                <label for="auth_token">Auth Token:</label>
                <p class="help-text">Your Cognito access token for authentication</p>
                <input type="text" name="auth_token" style="width:100%" placeholder="Bearer token..." />

                <label for="test_message">Test Message:</label>
                <p class="help-text">Test your configuration with a sample query</p>
                <input type="text" name="test_message" style="width:100%" placeholder="What would you like to explore today?" />
                
                <div style="margin-top: 2rem;">
                    <button type="submit" name="action" value="save">💾 Save Configuration</button>
                    <button type="submit" name="action" value="test">🧪 Test Configuration</button>
                </div>
            </div>
        </form>
        
        <script>
        // Auto-load config when auth token is provided
        document.querySelector('input[name="auth_token"]').addEventListener('blur', async function() {{
            const token = this.value.trim();
            if (!token) return;
            
            try {{
                const response = await fetch('/api/storage/api/memory/runtime-config', {{
                    headers: {{
                        'Authorization': token.startsWith('Bearer ') ? token : 'Bearer ' + token
                    }}
                }});
                
                if (response.ok) {{
                    const config = await response.json();
                    
                    // Update form fields with loaded config
                    document.querySelector('textarea[name="system_prompt"]').value = config.system_prompt || '';
                    document.querySelector('input[name="top_k"]').value = config.top_k_rag_hits || 5;
                    
                    // Update style selection
                    const styleSelect = document.querySelector('select[name="prompt_style"]');
                    styleSelect.value = config.prompt_style || 'default';
                    
                    // Update custom style modifier
                    document.querySelector('textarea[name="custom_style_modifier"]').value = config.custom_style_modifier || '';
                    
                    // Update model settings
                    const modelSelect = document.querySelector('select[name="model"]');
                    if (modelSelect) modelSelect.value = config.model || 'gpt-3.5-turbo';
                    
                    // Update temperature
                    const tempInput = document.querySelector('input[name="temperature"]');
                    if (tempInput) {{
                        tempInput.value = config.temperature || 0.7;
                        document.getElementById('temp-value').textContent = config.temperature || 0.7;
                    }}
                    
                    // Update other fields
                    const maxTokensInput = document.querySelector('input[name="max_tokens"]');
                    if (maxTokensInput) maxTokensInput.value = config.max_tokens || 1000;
                    
                    const presencePenaltyInput = document.querySelector('input[name="presence_penalty"]');
                    if (presencePenaltyInput) {{
                        presencePenaltyInput.value = config.presence_penalty || 0.1;
                        document.getElementById('presence-value').textContent = config.presence_penalty || 0.1;
                    }}
                    
                    const freqPenaltyInput = document.querySelector('input[name="frequency_penalty"]');
                    if (freqPenaltyInput) {{
                        freqPenaltyInput.value = config.frequency_penalty || 0.1;
                        document.getElementById('freq-value').textContent = config.frequency_penalty || 0.1;
                    }}
                    
                    // Update conversation history limit
                    const historyLimitInput = document.querySelector('input[name="conversation_history_limit"]');
                    if (historyLimitInput) historyLimitInput.value = config.conversation_history_limit || 5;
                    
                    toggleCustomStyle();
                    
                    // Show success message
                    alert('Configuration loaded successfully!');
                }} else {{
                    alert('Failed to load configuration. Check your token.');
                }}
            }} catch (error) {{
                console.error('Error loading config:', error);
                alert('Error loading configuration');
            }}
        }});
        
        // For production, adjust API URL
        if (window.location.hostname !== 'localhost') {{
            // Update fetch URL for production
            const originalFetch = window.fetch;
            window.fetch = function(url, options) {{
                if (url.startsWith('/api/storage/')) {{
                    // Already has correct prefix for production
                    return originalFetch.call(this, url, options);
                }}
                return originalFetch.call(this, url, options);
            }};
        }} else {{
            // For development, update URLs
            const originalFetch = window.fetch;
            window.fetch = function(url, options) {{
                if (url === '/api/storage/api/memory/runtime-config') {{
                    url = 'http://localhost:8011/api/memory/runtime-config';
                }}
                return originalFetch.call(this, url, options);
            }};
        }}
        </script>
    </body>
    </html>
    """

from fastapi import Form

@app.post("/admin", response_class=HTMLResponse)
async def save_config_ui(
    system_prompt: Optional[str] = Form(None),
    top_k: Optional[int] = Form(None),
    prompt_style: Optional[str] = Form(None),
    custom_style_modifier: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    temperature: Optional[float] = Form(None),
    max_tokens: Optional[int] = Form(None),
    presence_penalty: Optional[float] = Form(None),
    frequency_penalty: Optional[float] = Form(None),
    conversation_history_limit: Optional[int] = Form(None),
    auth_token: Optional[str] = Form(None),
    test_message: Optional[str] = Form(None),
    action: Optional[str] = Form(None),
):
    payload = None
    test_output = None
    status_message = None
    
    # Initialize style variables with defaults
    prompt_style = prompt_style or "default"
    custom_style_modifier = custom_style_modifier or ""

    if not system_prompt and auth_token:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(f"{STORAGE_URL}/api/memory/runtime-config")
                cfg = resp.json()
                system_prompt = cfg.get("system_prompt", "")
                top_k = top_k or cfg.get("top_k_rag_hits", 5)
                prompt_style = prompt_style or cfg.get("prompt_style", "default")
                custom_style_modifier = custom_style_modifier or cfg.get("custom_style_modifier", "")
                model = model or cfg.get("model", "gpt-3.5-turbo")
                temperature = temperature or cfg.get("temperature", 0.7)
                max_tokens = max_tokens or cfg.get("max_tokens", 1000)
                presence_penalty = presence_penalty or cfg.get("presence_penalty", 0.1)
                frequency_penalty = frequency_penalty or cfg.get("frequency_penalty", 0.1)
                conversation_history_limit = conversation_history_limit or cfg.get("conversation_history_limit", 5)
            except Exception:
                system_prompt = ""
                top_k = 5
                prompt_style = "default"
                custom_style_modifier = ""
                model = "gpt-3.5-turbo"
                temperature = 0.7
                max_tokens = 1000
                presence_penalty = 0.1
                frequency_penalty = 0.1
                conversation_history_limit = 5

    # 1. Save updated config
    if action == "save":
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{STORAGE_URL}/api/memory/runtime-config",
                headers=headers,
                json={
                    "system_prompt": system_prompt,
                    "conversation_history_limit": conversation_history_limit,
                    "top_k_rag_hits": top_k,
                    "prompt_style": prompt_style,
                    "custom_style_modifier": custom_style_modifier,
                    "model": model,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "presence_penalty": presence_penalty,
                    "frequency_penalty": frequency_penalty
                }
            )
            if resp.status_code == 200:
                status_message = "✅ Configuration saved successfully."
            else:
                status_message = f"❌ Save failed: {resp.status_code} — {await resp.aread()}"

    # 2. Run test
    if action == "test" and auth_token and test_message:
        try:
            payload = {
                "userId": "debug-user",
                "username": "test",
                "fullName": "Admin Tester",
                "traitScores": {"creative": 7, "logical": 6, "emotional": 8},
                "message": test_message,
                "sessionId": "debug-session",
                "systemPrompt": system_prompt,
                "topK_RAG_hits": top_k,
            }
            async with httpx.AsyncClient() as client:
                # Seed an empty session for test
                await client.post(
                    f"{STORAGE_URL}/api/memory/session-memory",
                    json={
                        "uuid": "debug-session",
                        "conversation_log": {"exchanges": []}
                    }
                )
                test_prompt = payload.copy()
                test_prompt["message"] = "[Prompt not visible]"
                query_resp = await client.post(
                    f"{os.getenv('CHAT_SERVICE_URL', 'http://localhost:8015')}/query",
                    headers={"Authorization": f"Bearer {auth_token}"},
                    json=payload
                )
                if query_resp.status_code == 200:
                    test_output = query_resp.json().get("answer", "[No answer returned]")
                else:
                    test_output = f"[Error {query_resp.status_code}]: {query_resp.text}"
        except Exception as e:
            test_output = f"Test failed: {e}"
    # Refresh config from storage after test or save to pre-populate form fields
    if auth_token:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{STORAGE_URL}/api/memory/runtime-config",
                    headers={"Authorization": f"Bearer {auth_token}"}
                )
                if resp.status_code == 200:
                    cfg = resp.json()
                    system_prompt = cfg.get("system_prompt", system_prompt)
                    top_k = cfg.get("top_k_rag_hits", top_k)
                    prompt_style = cfg.get("prompt_style", prompt_style)
                    custom_style_modifier = cfg.get("custom_style_modifier", custom_style_modifier)
            except Exception:
                pass  # Keep existing values if fetch fails

    # Render HTML output with same styling as GET
    return f"""
    <html>
    <head>
        <title>Xavigate Admin Panel</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1000px; margin: 0 auto; padding: 2rem; background: #f5f5f5; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem; }}
            h1 {{ margin: 0; font-size: 2rem; }}
            .subtitle {{ opacity: 0.9; margin-top: 0.5rem; }}
            .card {{ background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 2rem; }}
            .card h2 {{ margin-top: 0; color: #333; border-bottom: 2px solid #eee; padding-bottom: 1rem; }}
            .status {{ margin: 1rem 0; padding: 1rem; border-radius: 5px; }}
            .status.success {{ background-color: #c6f6d5; border-left: 4px solid #48bb78; color: #22543d; }}
            .status.error {{ background-color: #fed7d7; border-left: 4px solid #f56565; color: #742a2a; }}
            textarea {{ width: 100%; min-height: 200px; font-family: monospace; padding: 1rem; border: 1px solid #ddd; border-radius: 5px; resize: vertical; }}
            input, select {{ padding: 0.75rem; font-size: 1rem; border: 1px solid #ddd; border-radius: 5px; }}
            input[type="number"] {{ width: 120px; }}
            input[type="range"] {{ width: 300px; }}
            .range-container {{ display: flex; align-items: center; gap: 1rem; }}
            .range-value {{ font-weight: bold; min-width: 50px; }}
            select {{ width: 250px; }}
            button {{ padding: 0.75rem 2rem; font-size: 1rem; border: none; border-radius: 5px; cursor: pointer; margin-right: 1rem; }}
            button[value="save"] {{ background: #667eea; color: white; }}
            button[value="test"] {{ background: #48bb78; color: white; }}
            button:hover {{ opacity: 0.9; }}
            label {{ display: block; margin-top: 1.5rem; margin-bottom: 0.5rem; font-weight: 600; color: #444; }}
            .help-text {{ font-size: 0.875rem; color: #666; margin-top: 0.25rem; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }}
            .output {{ background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 1rem; margin-top: 1rem; }}
            pre {{ white-space: pre-wrap; word-wrap: break-word; }}
            @media (max-width: 768px) {{ .grid {{ grid-template-columns: 1fr; }} }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🧭 Xavigate Admin Panel</h1>
            <p class="subtitle">Configure AI behavior, prompting, and system parameters</p>
        </div>
        {f'<div class="status {"success" if status_message and "✅" in status_message else "error"}">{status_message}</div>' if status_message else ''}
        <form method="POST" action="/admin">
            <label>System Prompt:</label><br>
            <textarea name="system_prompt" rows="10" cols="80">{system_prompt or ""}</textarea><br><br>

            <label>Top K:</label><br>
            <input type="number" name="top_k" value="{top_k or 5}" min="1" max="10"><br><br>

            <label>Prompt Style:</label><br>
            <select name="prompt_style" style="width: 200px; padding: 0.5rem;">
                <option value="default" {"selected" if prompt_style == "default" else ""}>Default</option>
                <option value="empathetic" {"selected" if prompt_style == "empathetic" else ""}>Empathetic</option>
                <option value="analytical" {"selected" if prompt_style == "analytical" else ""}>Analytical</option>
                <option value="motivational" {"selected" if prompt_style == "motivational" else ""}>Motivational</option>
                <option value="socratic" {"selected" if prompt_style == "socratic" else ""}>Socratic</option>
                <option value="custom" {"selected" if prompt_style == "custom" else ""}>Custom</option>
            </select><br><br>

            <label>Custom Style Instructions (if custom selected):</label><br>
            <textarea name="custom_style_modifier" rows="3" cols="80">{custom_style_modifier or ""}</textarea><br><br>

            <label>Auth Token:</label><br>
            <input type="text" name="auth_token" style="width:100%" value="{auth_token or ''}"><br><br>

            <label>Test Prompt:</label><br>
            <input type="text" name="test_message" style="width:100%" value="{test_message or ''}"><br><br>

            <button type="submit" name="action" value="save">💾 Save Config</button>
            <button type="submit" name="action" value="test">▶️ Run Test Prompt</button>
        </form>
        {f'<div style="color: red; margin-top: 1rem;">⚠️ Auth token required to view current config.</div>' if not auth_token else ''}

        <hr>
        <h3>Test Output:</h3>
        <div style="width: 100%; max-height: 300px; overflow: auto; border: 1px solid #ccc; padding: 1rem; font-family: monospace; background-color: #f9f9f9;">
            {test_output or "—"}
        </div>
        <hr>
        <h3>Final Prompt Sent:</h3>
        <div style="width: 100%; max-height: 300px; overflow: auto; border: 1px solid #ccc; padding: 1rem; font-family: monospace; background-color: #f9f9f9;">
            {json.dumps(payload, indent=2) if payload else "—"}
        </div>
        <hr>
    </body></html>
    """