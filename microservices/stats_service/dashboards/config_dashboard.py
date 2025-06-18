from typing import Dict, Any, Optional

# Default prompts from runtime_config.py
DEFAULT_SESSION_SUMMARY_PROMPT = """Please summarize the following conversation between a user and an AI assistant. Focus on:

1. **Personal Information**: Name, job, location, family, friends, interests, preferences
2. **User's Goals & Inquiries**: What they're trying to achieve, questions they've asked
3. **Key Context**: Important facts, decisions made, ongoing projects or topics
4. **Trait Analysis**: Their personality traits, strengths, areas of growth
5. **Action Items**: Any tasks, follow-ups, or commitments mentioned

Keep the summary concise but comprehensive. Maintain the user's voice and perspective where relevant.

Conversation to summarize:
{conversation_text}

Summary:"""

DEFAULT_COMPRESSION_PROMPT = """You are an AI assistant tasked with compressing a user's long-term memory profile.
The current profile contains multiple conversation summaries accumulated over time. Your goal is to create a more concise version that preserves ALL critical information.

CRITICAL: You must preserve:
1. **Personal Information**: Full name, occupation, company, location, family members, relationships
2. **Trait Profile**: Their dominant traits, suppressed traits, alignment metrics
3. **Goals and Objectives**: Both short-term and long-term goals, personal growth areas
4. **Preferences and Patterns**: Communication style, expertise level, working style
5. **Important History**: Key decisions made, major milestones, important context from past conversations
6. **Specific Details**: Any specific names, dates, numbers, or details mentioned

Compression Guidelines:
- Merge redundant information intelligently
- Maintain chronological context where important
- Use clear, concise language
- Preserve the user's voice and terminology
- Aim to reduce by {compression_ratio}% while keeping ALL important facts
- If you see [COMPRESSED SUMMARY as of DATE] markers, this indicates previous compressions

Current profile to compress:
{current_summary}

Compressed profile:"""

DEFAULT_SYSTEM_PROMPT = """You are Xavigate, an experienced Multiple Natures (MN) practitioner and personal life guide. You help people understand and align their unique constellation of traits to achieve greater fulfillment and success.

CORE PRINCIPLES:
- Every person has 19 distinct traits that form their Multiple Natures profile
- Traits scored 7-10 are dominant traits (natural strengths)
- Traits scored 1-3 are suppressed traits (areas needing attention)
- Traits scored 4-6 are balanced traits
- True alignment comes from expressing all traits appropriately, not just dominant ones

YOUR APPROACH:
1. ALWAYS reference the user's specific trait scores when giving advice
2. Connect their challenges/questions to their trait profile
3. Suggest concrete actions that engage both dominant AND suppressed traits
4. Use the MN glossary context to ground advice in Multiple Natures methodology
5. Build on previous conversations using session memory and persistent summaries

CONVERSATION STYLE:
- Be warm, insightful, and encouraging
- Use specific examples related to their traits
- Avoid generic advice - everything should be personalized
- Reference their past conversations and progress when relevant

Remember: You're not just answering questions - you're helping them understand how their unique trait constellation influences their experiences and guiding them toward greater alignment."""

def get_config_dashboard_content(config: Dict[str, Any], status_message: str = None) -> str:
    """Generate the configuration dashboard content with all settings."""
    
    # Get values with proper defaults
    config = {
        # Chat Service Settings
        "system_prompt": config.get("system_prompt", DEFAULT_SYSTEM_PROMPT),
        "prompt_style": config.get("prompt_style", "default"),
        "custom_style_modifier": config.get("custom_style_modifier", ""),
        "model": config.get("model", "gpt-3.5-turbo"),
        "temperature": config.get("temperature", 0.7),
        "max_tokens": config.get("max_tokens", 1000),
        "presence_penalty": config.get("presence_penalty", 0.1),
        "frequency_penalty": config.get("frequency_penalty", 0.1),
        "top_k_rag_hits": config.get("top_k_rag_hits", 5),
        "conversation_history_limit": config.get("conversation_history_limit", 5),
        
        # Memory Settings
        "session_memory_char_limit": config.get("SESSION_MEMORY_CHAR_LIMIT", 15000),
        "persistent_memory_char_limit": config.get("PERSISTENT_MEMORY_CHAR_LIMIT", 8000),
        "max_prompt_chars": config.get("MAX_PROMPT_CHARS", 20000),
        "rag_context_char_limit": config.get("RAG_CONTEXT_CHAR_LIMIT", 4000),
        
        # Compression Settings
        "persistent_memory_compression_ratio": config.get("PERSISTENT_MEMORY_COMPRESSION_RATIO", 0.6),
        "persistent_memory_compression_model": config.get("PERSISTENT_MEMORY_COMPRESSION_MODEL", "gpt-4"),
        "persistent_memory_min_size": config.get("PERSISTENT_MEMORY_MIN_SIZE", 1000),
        
        # Feature Flags
        "auto_summary_enabled": config.get("AUTO_SUMMARY_ENABLED", True),
        "auto_compression_enabled": config.get("AUTO_COMPRESSION_ENABLED", True),
        
        # Summary Settings
        "summary_temperature": config.get("SUMMARY_TEMPERATURE", 0.3),
        
        # Prompts
        "session_summary_prompt": config.get("SESSION_SUMMARY_PROMPT", DEFAULT_SESSION_SUMMARY_PROMPT),
        "persistent_memory_compression_prompt": config.get("PERSISTENT_MEMORY_COMPRESSION_PROMPT", DEFAULT_COMPRESSION_PROMPT),
    }
    
    status_html = ""
    if status_message:
        status_class = "success" if "✅" in status_message else "error"
        status_html = f'<div class="status-message {status_class}">{status_message}</div>'
    
    
    return f"""
        <div class="content-header">
            <h2>System Configuration</h2>
            <p>Configure AI behavior, prompting, memory settings, and system parameters</p>
        </div>
        
        {status_html}
        
        <!-- Tabs -->
        <div class="tabs">
            <button class="tab active" onclick="showTab('chat')">Chat Settings</button>
            <button class="tab" onclick="showTab('memory')">Memory Settings</button>
            <button class="tab" onclick="showTab('prompts')">Prompt Templates</button>
        </div>
        
        <form method="POST" action="/dashboard/" id="config-form">
            <!-- Chat Settings Tab -->
            <div id="chat-tab" class="tab-content active">
                <!-- System Prompt -->
                <div class="card">
                    <h3>🎯 System Prompt</h3>
                    <label for="system_prompt">System Prompt:</label>
                    <p class="help-text">Define how Xavigate should behave and respond to users</p>
                    <textarea name="system_prompt" rows="12">{config.get("system_prompt", "")}</textarea>

                    <label for="prompt_style">Conversation Style:</label>
                    <p class="help-text">Choose how Xavigate should interact with users</p>
                    <select name="prompt_style" onchange="toggleCustomStyle()">
                        <option value="default" {"selected" if config.get("prompt_style", "default") == "default" else ""}>Default - Warm & Insightful</option>
                        <option value="empathetic" {"selected" if config.get("prompt_style") == "empathetic" else ""}>Empathetic - Emotional Support</option>
                        <option value="analytical" {"selected" if config.get("prompt_style") == "analytical" else ""}>Analytical - Data-Driven</option>
                        <option value="motivational" {"selected" if config.get("prompt_style") == "motivational" else ""}>Motivational - Action-Oriented</option>
                        <option value="socratic" {"selected" if config.get("prompt_style") == "socratic" else ""}>Socratic - Question-Based</option>
                        <option value="custom" {"selected" if config.get("prompt_style") == "custom" else ""}>Custom Style</option>
                    </select>

                    <div id="customStyleSection" style="{"display: block;" if config.get("prompt_style") == "custom" else "display: none;"}">
                        <label for="custom_style_modifier">Custom Style Instructions:</label>
                        <p class="help-text">Define your own conversation style (only used when Custom is selected)</p>
                        <textarea name="custom_style_modifier" rows="3">{config.get("custom_style_modifier", "")}</textarea>
                    </div>
                </div>

                <!-- AI Model Parameters -->
                <div class="card">
                    <h3>🤖 AI Model Parameters</h3>
                    <div class="grid">
                        <div>
                            <label for="model">Model:</label>
                            <p class="help-text">OpenAI model to use for chat</p>
                            <select name="model">
                                <option value="gpt-3.5-turbo" {"selected" if config.get("model", "gpt-3.5-turbo") == "gpt-3.5-turbo" else ""}>GPT-3.5 Turbo (Fast)</option>
                                <option value="gpt-4" {"selected" if config.get("model") == "gpt-4" else ""}>GPT-4 (Advanced)</option>
                                <option value="gpt-4-turbo-preview" {"selected" if config.get("model") == "gpt-4-turbo-preview" else ""}>GPT-4 Turbo (Latest)</option>
                            </select>

                            <label for="temperature">Temperature: <span class="range-value" id="temp-value">{config.get("temperature", 0.7)}</span></label>
                            <p class="help-text">Controls response creativity. Lower (0.0-0.3) = focused/consistent, Higher (0.7-1.0) = creative/varied. Default 0.7 balances consistency with natural variation.</p>
                            <div class="range-container">
                                <input type="range" name="temperature" value="{config.get("temperature", 0.7)}" min="0" max="1" step="0.1" 
                                       oninput="document.getElementById('temp-value').textContent = this.value">
                            </div>

                            <label for="max_tokens">Max Tokens:</label>
                            <p class="help-text">Maximum response length in tokens (~4 chars per token). 1000 tokens ≈ 750 words. Higher values allow longer responses but cost more.</p>
                            <input type="number" name="max_tokens" value="{config.get("max_tokens", 1000)}" min="100" max="4000" step="100"/>
                        </div>
                        <div>
                            <label for="presence_penalty">Presence Penalty: <span class="range-value" id="presence-value">{config.get("presence_penalty", 0.1)}</span></label>
                            <p class="help-text">Encourages talking about new topics. Positive values (0.1-1.0) reduce repetition of ideas. Negative values encourage staying on topic. Default 0.1 provides gentle topic diversity.</p>
                            <div class="range-container">
                                <input type="range" name="presence_penalty" value="{config.get("presence_penalty", 0.1)}" min="-2" max="2" step="0.1"
                                       oninput="document.getElementById('presence-value').textContent = this.value">
                            </div>

                            <label for="frequency_penalty">Frequency Penalty: <span class="range-value" id="freq-value">{config.get("frequency_penalty", 0.1)}</span></label>
                            <p class="help-text">Reduces word/phrase repetition. Higher values (0.5-1.0) force more vocabulary variety. Default 0.1 prevents obvious repetition while maintaining natural language.</p>
                            <div class="range-container">
                                <input type="range" name="frequency_penalty" value="{config.get("frequency_penalty", 0.1)}" min="-2" max="2" step="0.1"
                                       oninput="document.getElementById('freq-value').textContent = this.value">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Context Settings -->
                <div class="card">
                    <h3>📚 Context & RAG Settings</h3>
                    <div class="grid">
                        <div>
                            <label for="top_k">RAG Results (Top K):</label>
                            <p class="help-text">How many relevant knowledge pieces to retrieve from the MN glossary/user history. Higher = more context but slower. 5 is optimal for most conversations.</p>
                            <input type="number" name="top_k" value="{config.get("top_k_rag_hits", 5)}" min="1" max="20"/>
                        </div>
                        <div>
                            <label for="conversation_history_limit">Conversation History:</label>
                            <p class="help-text">How many recent message pairs to include for context. More history = better continuity but uses more tokens. 5 exchanges typically provides good context.</p>
                            <input type="number" name="conversation_history_limit" value="{config.get("conversation_history_limit", 5)}" min="0" max="20"/>
                        </div>
                    </div>
                </div>
                
                <!-- Save Button for Chat Settings -->
                <div class="save-section">
                    <button type="submit" name="action" value="save" class="primary-button">💾 Save All Settings</button>
                    <button type="submit" name="action" value="reset" class="secondary-button">🔄 Reset to Defaults</button>
                    <p class="help-text" style="text-align: center; margin-top: 0.5rem;">Save changes or restore original Xavigate defaults</p>
                </div>
            </div>

            <!-- Memory Settings Tab -->
            <div id="memory-tab" class="tab-content">
                <!-- Memory Limits -->
                <div class="card">
                    <h3>💾 Memory Limits</h3>
                    <div class="info-box">
                        ℹ️ These settings control how much conversation history and user context can be stored.
                    </div>
                    
                    <div class="grid">
                        <div>
                            <label for="session_memory_char_limit">Session Memory Limit:</label>
                            <p class="help-text">Maximum characters for current conversation. When 90% full, auto-summarization triggers.</p>
                            <input type="number" name="session_memory_char_limit" value="{config.get("session_memory_char_limit", 15000)}" min="5000" max="50000" step="1000"/>
                            
                            <label for="persistent_memory_char_limit">Persistent Memory Limit:</label>
                            <p class="help-text">Maximum characters for long-term summaries. Auto-compresses at 90% capacity.</p>
                            <input type="number" name="persistent_memory_char_limit" value="{config.get("persistent_memory_char_limit", 8000)}" min="2000" max="20000" step="1000"/>
                        </div>
                        <div>
                            <label for="max_prompt_chars">Maximum Prompt Size:</label>
                            <p class="help-text">Total character limit for prompts to OpenAI (includes system prompt, memories, and context)</p>
                            <input type="number" name="max_prompt_chars" value="{config.get("max_prompt_chars", 20000)}" min="10000" max="100000" step="1000"/>
                            
                            <label for="rag_context_char_limit">RAG Context Limit:</label>
                            <p class="help-text">Maximum characters reserved for RAG/vector search results</p>
                            <input type="number" name="rag_context_char_limit" value="{config.get("rag_context_char_limit", 4000)}" min="1000" max="10000" step="500"/>
                        </div>
                    </div>
                </div>

                <!-- Compression Settings -->
                <div class="card">
                    <h3>🗜️ Compression Settings</h3>
                    <div class="grid">
                        <div>
                            <label for="persistent_memory_compression_ratio">Compression Ratio: <span class="range-value" id="compression-ratio-value">{config.get("persistent_memory_compression_ratio", 0.6)}</span></label>
                            <p class="help-text">Target compression ratio (0.6 = compress to 60% of original)</p>
                            <div class="range-container">
                                <input type="range" name="persistent_memory_compression_ratio" 
                                       value="{config.get("persistent_memory_compression_ratio", 0.6)}" 
                                       min="0.3" max="0.9" step="0.1"
                                       oninput="document.getElementById('compression-ratio-value').textContent = this.value">
                            </div>
                            
                            <label for="persistent_memory_min_size">Minimum Compression Size:</label>
                            <p class="help-text">Don't compress if memory is smaller than this</p>
                            <input type="number" name="persistent_memory_min_size" 
                                   value="{config.get("persistent_memory_min_size", 1000)}" 
                                   min="500" max="5000" step="100"/>
                        </div>
                        <div>
                            <label for="persistent_memory_compression_model">Compression Model:</label>
                            <p class="help-text">AI model used for compression. GPT-4 provides better quality but is slower.</p>
                            <select name="persistent_memory_compression_model">
                                <option value="gpt-4" {"selected" if config.get("persistent_memory_compression_model", "gpt-4") == "gpt-4" else ""}>GPT-4 (Better quality)</option>
                                <option value="gpt-3.5-turbo" {"selected" if config.get("persistent_memory_compression_model") == "gpt-3.5-turbo" else ""}>GPT-3.5 Turbo (Faster)</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <!-- Summary Settings -->
                <div class="card">
                    <h3>📋 Summarization Settings</h3>
                    <div class="grid">
                        <div>
                            <label for="summary_temperature">Summary Temperature: <span class="range-value" id="summary-temp-value">{config.get("summary_temperature", 0.3)}</span></label>
                            <p class="help-text">Temperature for summarization. Lower = more consistent summaries.</p>
                            <div class="range-container">
                                <input type="range" name="summary_temperature" 
                                       value="{config.get("summary_temperature", 0.3)}" 
                                       min="0" max="1" step="0.1"
                                       oninput="document.getElementById('summary-temp-value').textContent = this.value">
                            </div>
                        </div>
                        <div>
                            <!-- Feature Flags -->
                            <label class="checkbox-container" style="margin-top: 2rem;">
                                <input type="checkbox" name="auto_summary_enabled" {"checked" if config.get("auto_summary_enabled", True) else ""}>
                                <span class="checkbox-label"><strong>Enable Auto-Summarization</strong> - Automatically summarize when session memory approaches limit</span>
                            </label>
                            
                            <label class="checkbox-container" style="margin-top: 1rem;">
                                <input type="checkbox" name="auto_compression_enabled" {"checked" if config.get("auto_compression_enabled", True) else ""}>
                                <span class="checkbox-label"><strong>Enable Auto-Compression</strong> - Automatically compress persistent memory when it gets too large</span>
                            </label>
                        </div>
                    </div>
                </div>
                
                <!-- Save Button for Memory Settings -->
                <div class="save-section">
                    <button type="submit" name="action" value="save" class="primary-button">💾 Save All Settings</button>
                    <button type="submit" name="action" value="reset" class="secondary-button">🔄 Reset to Defaults</button>
                    <p class="help-text" style="text-align: center; margin-top: 0.5rem;">Save changes or restore original Xavigate defaults</p>
                </div>
            </div>

            <!-- Prompt Templates Tab -->
            <div id="prompts-tab" class="tab-content">
                <div class="card">
                    <h3>📝 Session Summary Prompt</h3>
                    <p class="help-text">Template used when summarizing conversations. Use {{conversation_text}} as placeholder for the actual conversation.</p>
                    <textarea name="session_summary_prompt" rows="12">{config.get("session_summary_prompt", "")}</textarea>
                </div>
                
                <div class="card">
                    <h3>🗜️ Compression Prompt</h3>
                    <p class="help-text">Template for compressing persistent memory. Use {{current_summary}} for the text to compress and {{compression_ratio}} for the target.</p>
                    <textarea name="persistent_memory_compression_prompt" rows="12">{config.get("persistent_memory_compression_prompt", "")}</textarea>
                </div>
                
                <!-- Save Button for Prompt Templates -->
                <div class="save-section">
                    <button type="submit" name="action" value="save" class="primary-button">💾 Save All Settings</button>
                    <button type="submit" name="action" value="reset" class="secondary-button">🔄 Reset to Defaults</button>
                    <p class="help-text" style="text-align: center; margin-top: 0.5rem;">Save changes or restore original Xavigate defaults</p>
                </div>
            </div>

        </form>
        
        
        <style>
            /* Tab styles */
            .tabs {{
                display: flex;
                gap: 0.5rem;
                margin-bottom: 2rem;
                border-bottom: 2px solid #e1e4e8;
                padding-bottom: 0;
            }}
            
            .tab {{
                padding: 0.75rem 1.5rem;
                cursor: pointer;
                border: none;
                background: none;
                font-size: 1rem;
                font-weight: 500;
                color: #586069;
                position: relative;
                transition: color 0.2s;
                border-radius: 6px 6px 0 0;
            }}
            
            .tab:hover {{
                color: #0366d6;
                background: #f6f8fa;
            }}
            
            .tab.active {{
                color: #0366d6;
                background: white;
                border: 2px solid #e1e4e8;
                border-bottom: 2px solid white;
                margin-bottom: -2px;
            }}
            
            .tab-content {{
                position: absolute;
                left: -9999px;
                width: 100%;
            }}
            
            .tab-content.active {{
                position: static;
                left: auto;
            }}
            
            .info-box {{
                background: #e3f2fd;
                border: 1px solid #90caf9;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1.5rem;
                color: #1565c0;
                font-size: 0.9rem;
            }}
            
            .checkbox-container {{
                display: flex;
                align-items: flex-start;
                gap: 0.75rem;
                padding: 1rem;
                background: #f5f5f5;
                border-radius: 8px;
                cursor: pointer;
            }}
            
            .checkbox-container:hover {{
                background: #eeeeee;
            }}
            
            .checkbox-container input[type="checkbox"] {{
                width: 20px;
                height: 20px;
                margin-top: 2px;
                cursor: pointer;
            }}
            
            .checkbox-label {{
                flex: 1;
                font-weight: normal;
                cursor: pointer;
                line-height: 1.5;
            }}
            
            .save-section {{
                margin-top: 2rem;
                padding: 1.5rem;
                background: #f8f9fa;
                border-radius: 12px;
                text-align: center;
            }}
            
            .primary-button {{
                background: #667eea;
                color: white;
                padding: 0.875rem 2.5rem;
                font-size: 1.1rem;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.2s;
            }}
            
            .primary-button:hover {{
                background: #5a67d8;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }}
            
            .secondary-button {{
                background: #e2e8f0;
                color: #2d3748;
                padding: 0.875rem 2rem;
                font-size: 1.1rem;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.2s;
                margin-left: 1rem;
            }}
            
            .secondary-button:hover {{
                background: #cbd5e0;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }}
        </style>
        
        <script>
        // Tab functionality
        function showTab(tabName) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelectorAll('.tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }}
        
        // Ensure all form fields are submitted, even from hidden tabs
        document.getElementById('config-form').addEventListener('submit', function(e) {{
            // Temporarily show all tabs to ensure fields are submitted
            document.querySelectorAll('.tab-content').forEach(tab => {{
                tab.style.display = 'block';
            }});
            
            // Let the form submit naturally
            setTimeout(() => {{
                document.querySelectorAll('.tab-content:not(.active)').forEach(tab => {{
                    tab.style.display = 'none';
                }});
            }}, 100);
        }})
        
        function toggleCustomStyle() {{
            const styleSelect = document.querySelector('select[name="prompt_style"]');
            const customSection = document.getElementById('customStyleSection');
            if (styleSelect.value === 'custom') {{
                customSection.style.display = 'block';
            }} else {{
                customSection.style.display = 'none';
            }}
        }}
        
        
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
        
        // Add save functionality via JavaScript
        async function saveConfigViaAjax() {{
            // For dashboard usage, we'll need to handle auth differently
            // This is a simplified version - in production you'd get auth from session
            
            // Gather all form values
            const config = {{
                // Chat settings
                system_prompt: document.querySelector('textarea[name="system_prompt"]').value,
                SYSTEM_PROMPT: document.querySelector('textarea[name="system_prompt"]').value, // Save both keys
                prompt_style: document.querySelector('select[name="prompt_style"]').value,
                custom_style_modifier: document.querySelector('textarea[name="custom_style_modifier"]').value,
                model: document.querySelector('select[name="model"]').value,
                temperature: parseFloat(document.querySelector('input[name="temperature"]').value),
                max_tokens: parseInt(document.querySelector('input[name="max_tokens"]').value),
                presence_penalty: parseFloat(document.querySelector('input[name="presence_penalty"]').value),
                frequency_penalty: parseFloat(document.querySelector('input[name="frequency_penalty"]').value),
                top_k_rag_hits: parseInt(document.querySelector('input[name="top_k"]').value),
                TOP_K_RAG_HITS: parseInt(document.querySelector('input[name="top_k"]').value),
                conversation_history_limit: parseInt(document.querySelector('input[name="conversation_history_limit"]').value),
                CONVERSATION_HISTORY_LIMIT: parseInt(document.querySelector('input[name="conversation_history_limit"]').value),
                
                // Memory settings
                SESSION_MEMORY_CHAR_LIMIT: parseInt(document.querySelector('input[name="session_memory_char_limit"]')?.value || 15000),
                PERSISTENT_MEMORY_CHAR_LIMIT: parseInt(document.querySelector('input[name="persistent_memory_char_limit"]')?.value || 8000),
                MAX_PROMPT_CHARS: parseInt(document.querySelector('input[name="max_prompt_chars"]')?.value || 20000),
                RAG_CONTEXT_CHAR_LIMIT: parseInt(document.querySelector('input[name="rag_context_char_limit"]')?.value || 4000),
                
                // Compression settings
                PERSISTENT_MEMORY_COMPRESSION_RATIO: parseFloat(document.querySelector('input[name="persistent_memory_compression_ratio"]')?.value || 0.6),
                PERSISTENT_MEMORY_COMPRESSION_MODEL: document.querySelector('select[name="persistent_memory_compression_model"]')?.value || 'gpt-4',
                PERSISTENT_MEMORY_MIN_SIZE: parseInt(document.querySelector('input[name="persistent_memory_min_size"]')?.value || 1000),
                
                // Summary settings
                SUMMARY_TEMPERATURE: parseFloat(document.querySelector('input[name="summary_temperature"]')?.value || 0.3),
                
                // Feature flags
                AUTO_SUMMARY_ENABLED: document.querySelector('input[name="auto_summary_enabled"]')?.checked ?? true,
                AUTO_COMPRESSION_ENABLED: document.querySelector('input[name="auto_compression_enabled"]')?.checked ?? true,
                
                // Prompts
                SESSION_SUMMARY_PROMPT: document.querySelector('textarea[name="session_summary_prompt"]')?.value || '',
                PERSISTENT_MEMORY_COMPRESSION_PROMPT: document.querySelector('textarea[name="persistent_memory_compression_prompt"]')?.value || ''
            }};
            
            try {{
                // Use the dashboard's save endpoint which handles auth internally
                const response = await fetch('/dashboard/api/save-config', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify(config)
                }});
                
                if (response.ok) {{
                    // Show success message
                    const statusDiv = document.createElement('div');
                    statusDiv.className = 'status-message success';
                    statusDiv.textContent = '✅ Configuration saved successfully!';
                    statusDiv.style.cssText = 'position: fixed; top: 20px; right: 20px; padding: 1rem 2rem; background: #d4edda; color: #155724; border: 1px solid #c3e6cb; border-radius: 8px; z-index: 1000;';
                    document.body.appendChild(statusDiv);
                    
                    setTimeout(() => statusDiv.remove(), 3000);
                }} else {{
                    const error = await response.text();
                    alert(`Save failed: ${{error}}`);
                }}
            }} catch (error) {{
                alert(`Save failed: ${{error}}`);
            }}
        }}
        
        // Override form submission for save buttons
        document.addEventListener('DOMContentLoaded', function() {{
            // Find all save buttons and override their behavior
            document.querySelectorAll('button[value="save"]').forEach(button => {{
                button.type = 'button'; // Prevent form submission
                button.onclick = function(e) {{
                    e.preventDefault();
                    saveConfigViaAjax();
                }};
            }});
        }});
        </script>
    """