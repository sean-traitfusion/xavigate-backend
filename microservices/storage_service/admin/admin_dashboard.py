"""
Comprehensive admin dashboard for Xavigate configuration
Integrates all memory, chat, and AI settings in one place
"""
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional, Dict, Any
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import runtime_config

router = APIRouter()

ADMIN_DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Xavigate Admin Dashboard</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f2f5;
            color: #1a1a1a;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .header h1 {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            font-size: 2rem;
            font-weight: 600;
        }
        .header p {
            max-width: 1200px;
            margin: 0.5rem auto 0;
            padding: 0 2rem;
            opacity: 0.9;
        }
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        .tabs {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            border-bottom: 2px solid #e1e4e8;
            flex-wrap: wrap;
        }
        .tab {
            padding: 0.75rem 1.5rem;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 1rem;
            font-weight: 500;
            color: #586069;
            position: relative;
            transition: color 0.2s;
        }
        .tab:hover { color: #0366d6; }
        .tab.active { color: #0366d6; }
        .tab.active::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            right: 0;
            height: 2px;
            background: #0366d6;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .section {
            background: white;
            border-radius: 8px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .section h2 {
            margin: 0 0 1.5rem 0;
            font-size: 1.5rem;
            color: #24292e;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .section-icon { font-size: 1.25rem; }
        .form-group {
            margin-bottom: 1.5rem;
        }
        label {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #24292e;
            font-size: 0.95rem;
        }
        .help-text {
            font-size: 0.875rem;
            color: #6a737d;
            margin-bottom: 0.5rem;
        }
        input[type="text"],
        input[type="number"],
        select,
        textarea {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #d1d5da;
            border-radius: 6px;
            font-size: 0.95rem;
            background: #fafbfc;
            transition: all 0.2s;
        }
        input:focus,
        select:focus,
        textarea:focus {
            outline: none;
            border-color: #0366d6;
            background: white;
            box-shadow: 0 0 0 3px rgba(3, 102, 214, 0.1);
        }
        textarea {
            min-height: 150px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.875rem;
            resize: vertical;
        }
        .range-group {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        input[type="range"] {
            flex: 1;
        }
        .range-value {
            min-width: 50px;
            font-weight: 600;
            color: #0366d6;
        }
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem;
            background: #f6f8fa;
            border-radius: 6px;
            cursor: pointer;
        }
        .checkbox-group:hover { background: #f0f2f5; }
        input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        button {
            padding: 0.75rem 2rem;
            font-size: 1rem;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-primary {
            background: #0366d6;
            color: white;
        }
        .btn-primary:hover {
            background: #0256c7;
            box-shadow: 0 2px 4px rgba(3, 102, 214, 0.3);
        }
        .btn-secondary {
            background: #6a737d;
            color: white;
            margin-left: 1rem;
        }
        .btn-secondary:hover {
            background: #586069;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        .stat-label {
            font-size: 0.875rem;
            opacity: 0.9;
        }
        .alert {
            padding: 1rem;
            border-radius: 6px;
            margin-bottom: 1rem;
            display: none;
        }
        .alert.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .style-option {
            margin-bottom: 0.5rem;
        }
        .info-box {
            background: #e3f2fd;
            border: 1px solid #90caf9;
            border-radius: 6px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            color: #1565c0;
            font-size: 0.875rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧭 Xavigate Admin Dashboard</h1>
        <p>Comprehensive configuration for memory, chat, and AI settings</p>
    </div>
    
    <div class="container">
        <div id="alert" class="alert"></div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="session-limit">{session_limit}</div>
                <div class="stat-label">Session Memory (chars)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="persistent-limit">{persistent_limit}</div>
                <div class="stat-label">Persistent Memory (chars)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="prompt-limit">{prompt_limit}</div>
                <div class="stat-label">Max Prompt (chars)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="rag-hits">{rag_hits}</div>
                <div class="stat-label">RAG Results</div>
            </div>
        </div>
        
        <form id="config-form" method="POST" action="/admin">
            <div class="tabs">
                <button type="button" class="tab active" onclick="showTab('chat')">Chat Settings</button>
                <button type="button" class="tab" onclick="showTab('memory')">Memory Settings</button>
                <button type="button" class="tab" onclick="showTab('prompts')">Prompts</button>
                <button type="button" class="tab" onclick="showTab('ai')">AI Models</button>
                <button type="button" class="tab" onclick="showTab('advanced')">Advanced</button>
            </div>
            
            <!-- Chat Settings Tab -->
            <div id="chat-tab" class="tab-content active">
                <div class="section">
                    <h2><span class="section-icon">💬</span> Chat Configuration</h2>
                    
                    <div class="form-group">
                        <label>System Prompt</label>
                        <p class="help-text">Main prompt that defines Xavigate's behavior and Multiple Natures approach</p>
                        <textarea name="SYSTEM_PROMPT" rows="12">{system_prompt}</textarea>
                    </div>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Conversation Style</label>
                            <p class="help-text">Choose how Xavigate interacts with users</p>
                            <select name="PROMPT_STYLE" onchange="toggleCustomStyle()">
                                <option value="default" {style_default}>Default - Warm & Insightful</option>
                                <option value="empathetic" {style_empathetic}>Empathetic - Emotional Support</option>
                                <option value="analytical" {style_analytical}>Analytical - Data-Driven</option>
                                <option value="motivational" {style_motivational}>Motivational - Action-Oriented</option>
                                <option value="socratic" {style_socratic}>Socratic - Question-Based</option>
                                <option value="custom" {style_custom}>Custom Style</option>
                            </select>
                        </div>
                        
                        <div class="form-group" id="custom-style-group" style="{custom_style_display}">
                            <label>Custom Style Instructions</label>
                            <p class="help-text">Define your own conversation style</p>
                            <textarea name="CUSTOM_STYLE_MODIFIER" rows="3">{custom_style_modifier}</textarea>
                        </div>
                    </div>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Conversation History Limit</label>
                            <p class="help-text">Number of previous exchanges to include in context</p>
                            <input type="number" name="CONVERSATION_HISTORY_LIMIT" value="{conversation_history_limit}" min="0" max="20">
                        </div>
                        
                        <div class="form-group">
                            <label>RAG Results (Top K)</label>
                            <p class="help-text">Number of knowledge base results to retrieve</p>
                            <input type="number" name="TOP_K_RAG_HITS" value="{top_k_rag_hits}" min="1" max="20">
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2><span class="section-icon">🤖</span> Chat Model Settings</h2>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Model</label>
                            <p class="help-text">OpenAI model for chat responses</p>
                            <select name="CHAT_MODEL">
                                <option value="gpt-3.5-turbo" {chat_model_35}>GPT-3.5 Turbo (Fast)</option>
                                <option value="gpt-4" {chat_model_4}>GPT-4 (Advanced)</option>
                                <option value="gpt-4-turbo-preview" {chat_model_4t}>GPT-4 Turbo (Latest)</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label>Max Tokens</label>
                            <p class="help-text">Maximum response length</p>
                            <input type="number" name="CHAT_MAX_TOKENS" value="{chat_max_tokens}" min="100" max="4000" step="100">
                        </div>
                    </div>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Temperature</label>
                            <p class="help-text">Controls randomness (0=focused, 1=creative)</p>
                            <div class="range-group">
                                <input type="range" name="CHAT_TEMPERATURE" value="{chat_temperature}" min="0" max="1" step="0.1" oninput="updateRangeValue('chat-temp', this.value)">
                                <span class="range-value" id="chat-temp-value">{chat_temperature}</span>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label>Presence Penalty</label>
                            <p class="help-text">Encourages new topics (-2 to 2)</p>
                            <div class="range-group">
                                <input type="range" name="CHAT_PRESENCE_PENALTY" value="{chat_presence_penalty}" min="-2" max="2" step="0.1" oninput="updateRangeValue('chat-presence', this.value)">
                                <span class="range-value" id="chat-presence-value">{chat_presence_penalty}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Memory Settings Tab -->
            <div id="memory-tab" class="tab-content">
                <div class="section">
                    <h2><span class="section-icon">💾</span> Memory Limits</h2>
                    
                    <div class="info-box">
                        ℹ️ These settings control how much conversation history and user context can be stored.
                    </div>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Session Memory Limit</label>
                            <p class="help-text">Maximum characters for current conversation</p>
                            <input type="number" name="SESSION_MEMORY_CHAR_LIMIT" value="{session_memory_limit}" min="5000" max="50000" step="1000">
                        </div>
                        
                        <div class="form-group">
                            <label>Persistent Memory Limit</label>
                            <p class="help-text">Maximum characters for long-term summaries</p>
                            <input type="number" name="PERSISTENT_MEMORY_CHAR_LIMIT" value="{persistent_memory_limit}" min="2000" max="20000" step="1000">
                        </div>
                    </div>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Max Prompt Size</label>
                            <p class="help-text">Total character limit for final prompt to AI</p>
                            <input type="number" name="MAX_PROMPT_CHARS" value="{max_prompt_chars}" min="10000" max="100000" step="1000">
                        </div>
                        
                        <div class="form-group">
                            <label>RAG Context Limit</label>
                            <p class="help-text">Maximum characters for knowledge base context</p>
                            <input type="number" name="RAG_CONTEXT_CHAR_LIMIT" value="{rag_context_limit}" min="1000" max="10000" step="500">
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2><span class="section-icon">🗜️</span> Compression Settings</h2>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Compression Ratio</label>
                            <p class="help-text">Target reduction percentage (0.1 = 10% of original)</p>
                            <div class="range-group">
                                <input type="range" name="PERSISTENT_MEMORY_COMPRESSION_RATIO" value="{compression_ratio}" min="0.1" max="0.9" step="0.05" oninput="updateRangeValue('compression', this.value)">
                                <span class="range-value" id="compression-value">{compression_ratio}</span>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label>Compression Model</label>
                            <p class="help-text">AI model for memory compression</p>
                            <select name="PERSISTENT_MEMORY_COMPRESSION_MODEL">
                                <option value="gpt-3.5-turbo" {comp_model_35}>GPT-3.5 Turbo</option>
                                <option value="gpt-4" {comp_model_4}>GPT-4 (Better quality)</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Min Size for Compression</label>
                            <p class="help-text">Don't compress if below this size</p>
                            <input type="number" name="PERSISTENT_MEMORY_MIN_SIZE" value="{min_compression_size}" min="500" max="5000" step="100">
                        </div>
                        
                        <div class="form-group">
                            <label>Max Compressions</label>
                            <p class="help-text">Maximum times to compress same content</p>
                            <input type="number" name="PERSISTENT_MEMORY_MAX_COMPRESSIONS" value="{max_compressions}" min="1" max="10">
                        </div>
                    </div>
                    
                    <div class="checkbox-group">
                        <input type="checkbox" name="AUTO_SUMMARY_ENABLED" id="auto-summary" {auto_summary_checked}>
                        <label for="auto-summary">Enable Auto-Summarization (at 90% capacity)</label>
                    </div>
                    
                    <div class="checkbox-group">
                        <input type="checkbox" name="AUTO_COMPRESSION_ENABLED" id="auto-compression" {auto_compression_checked}>
                        <label for="auto-compression">Enable Auto-Compression (at 90% capacity)</label>
                    </div>
                </div>
            </div>
            
            <!-- Prompts Tab -->
            <div id="prompts-tab" class="tab-content">
                <div class="section">
                    <h2><span class="section-icon">📝</span> Summary Prompts</h2>
                    
                    <div class="form-group">
                        <label>Session Summary Prompt</label>
                        <p class="help-text">Instructions for summarizing conversations</p>
                        <textarea name="SESSION_SUMMARY_PROMPT" rows="12">{session_summary_prompt}</textarea>
                    </div>
                    
                    <div class="form-group">
                        <label>Persistent Memory Compression Prompt</label>
                        <p class="help-text">Instructions for compressing long-term memory</p>
                        <textarea name="PERSISTENT_MEMORY_COMPRESSION_PROMPT" rows="12">{compression_prompt}</textarea>
                    </div>
                </div>
            </div>
            
            <!-- AI Models Tab -->
            <div id="ai-tab" class="tab-content">
                <div class="section">
                    <h2><span class="section-icon">⚙️</span> General AI Settings</h2>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Summary Model</label>
                            <p class="help-text">Model for generating summaries</p>
                            <select name="GPT_MODEL">
                                <option value="gpt-3.5-turbo" {gpt_model_35}>GPT-3.5 Turbo</option>
                                <option value="gpt-4" {gpt_model_4}>GPT-4</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label>Summary Temperature</label>
                            <p class="help-text">Lower = more consistent summaries</p>
                            <div class="range-group">
                                <input type="range" name="SUMMARY_TEMPERATURE" value="{summary_temperature}" min="0" max="1" step="0.1" oninput="updateRangeValue('summary-temp', this.value)">
                                <span class="range-value" id="summary-temp-value">{summary_temperature}</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2><span class="section-icon">🔧</span> OpenAI Default Settings</h2>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Default Model</label>
                            <p class="help-text">Fallback model for general operations</p>
                            <select name="OPENAI_MODEL">
                                <option value="gpt-3.5-turbo" {openai_model_35}>GPT-3.5 Turbo</option>
                                <option value="gpt-4" {openai_model_4}>GPT-4</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label>Default Max Tokens</label>
                            <p class="help-text">Maximum tokens for general operations</p>
                            <input type="number" name="OPENAI_MAX_TOKENS" value="{openai_max_tokens}" min="100" max="4000" step="100">
                        </div>
                    </div>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Default Temperature</label>
                            <p class="help-text">Controls randomness for general operations</p>
                            <div class="range-group">
                                <input type="range" name="OPENAI_TEMPERATURE" value="{openai_temperature}" min="0" max="2" step="0.1" oninput="updateRangeValue('openai-temp', this.value)">
                                <span class="range-value" id="openai-temp-value">{openai_temperature}</span>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label>Timeout (seconds)</label>
                            <p class="help-text">Maximum wait time for API responses</p>
                            <input type="number" name="OPENAI_TIMEOUT" value="{openai_timeout}" min="10" max="300" step="5">
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Advanced Tab -->
            <div id="advanced-tab" class="tab-content">
                <div class="section">
                    <h2><span class="section-icon">🔬</span> Advanced Settings</h2>
                    
                    <div class="info-box">
                        ⚠️ These settings affect system behavior. Change with caution.
                    </div>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Top P</label>
                            <p class="help-text">Nucleus sampling parameter</p>
                            <div class="range-group">
                                <input type="range" name="OPENAI_TOP_P" value="{openai_top_p}" min="0" max="1" step="0.05" oninput="updateRangeValue('top-p', this.value)">
                                <span class="range-value" id="top-p-value">{openai_top_p}</span>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label>Frequency Penalty</label>
                            <p class="help-text">Reduces repetition (-2 to 2)</p>
                            <div class="range-group">
                                <input type="range" name="OPENAI_FREQUENCY_PENALTY" value="{openai_frequency_penalty}" min="-2" max="2" step="0.1" oninput="updateRangeValue('freq-penalty', this.value)">
                                <span class="range-value" id="freq-penalty-value">{openai_frequency_penalty}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="grid-2">
                        <div class="form-group">
                            <label>Presence Penalty</label>
                            <p class="help-text">Encourages new topics (-2 to 2)</p>
                            <div class="range-group">
                                <input type="range" name="OPENAI_PRESENCE_PENALTY" value="{openai_presence_penalty}" min="-2" max="2" step="0.1" oninput="updateRangeValue('pres-penalty', this.value)">
                                <span class="range-value" id="pres-penalty-value">{openai_presence_penalty}</span>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label>Chat Frequency Penalty</label>
                            <p class="help-text">Frequency penalty for chat responses</p>
                            <div class="range-group">
                                <input type="range" name="CHAT_FREQUENCY_PENALTY" value="{chat_frequency_penalty}" min="-2" max="2" step="0.1" oninput="updateRangeValue('chat-freq', this.value)">
                                <span class="range-value" id="chat-freq-value">{chat_frequency_penalty}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e1e4e8;">
                <button type="submit" class="btn-primary">💾 Save Configuration</button>
                <button type="button" class="btn-secondary" onclick="resetForm()">↺ Reset to Defaults</button>
            </div>
        </form>
    </div>
    
    <script>
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }
        
        function updateRangeValue(id, value) {
            document.getElementById(id + '-value').textContent = value;
        }
        
        function toggleCustomStyle() {
            const styleSelect = document.querySelector('select[name="PROMPT_STYLE"]');
            const customGroup = document.getElementById('custom-style-group');
            
            if (styleSelect.value === 'custom') {
                customGroup.style.display = 'block';
            } else {
                customGroup.style.display = 'none';
            }
        }
        
        function resetForm() {
            if (confirm('Reset all settings to defaults? This cannot be undone.')) {
                window.location.href = '/admin/reset';
            }
        }
        
        // Initialize custom style visibility
        toggleCustomStyle();
        
        // Show success/error alerts from URL params
        const urlParams = new URLSearchParams(window.location.search);
        const alert = document.getElementById('alert');
        if (urlParams.get('success') === 'true') {
            alert.textContent = '✓ Configuration saved successfully!';
            alert.classList.add('success');
            alert.style.display = 'block';
            setTimeout(() => alert.style.display = 'none', 5000);
        } else if (urlParams.get('error')) {
            alert.textContent = '✗ Error: ' + urlParams.get('error');
            alert.classList.add('error');
            alert.style.display = 'block';
        }
    </script>
</body>
</html>
"""

@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard():
    """Serve the comprehensive admin dashboard"""
    config = runtime_config.all_config()
    
    # Prepare template variables
    template_vars = {
        # Stats
        "session_limit": f"{config.get('SESSION_MEMORY_CHAR_LIMIT', 15000):,}",
        "persistent_limit": f"{config.get('PERSISTENT_MEMORY_CHAR_LIMIT', 8000):,}",
        "prompt_limit": f"{config.get('MAX_PROMPT_CHARS', 20000):,}",
        "rag_hits": config.get('TOP_K_RAG_HITS', 5),
        
        # Chat settings
        "system_prompt": config.get('SYSTEM_PROMPT', ''),
        "prompt_style": config.get('PROMPT_STYLE', 'default'),
        "custom_style_modifier": config.get('CUSTOM_STYLE_MODIFIER', ''),
        "conversation_history_limit": config.get('CONVERSATION_HISTORY_LIMIT', 5),
        "top_k_rag_hits": config.get('TOP_K_RAG_HITS', 5),
        
        # Style selections
        "style_default": "selected" if config.get('PROMPT_STYLE', 'default') == 'default' else "",
        "style_empathetic": "selected" if config.get('PROMPT_STYLE') == 'empathetic' else "",
        "style_analytical": "selected" if config.get('PROMPT_STYLE') == 'analytical' else "",
        "style_motivational": "selected" if config.get('PROMPT_STYLE') == 'motivational' else "",
        "style_socratic": "selected" if config.get('PROMPT_STYLE') == 'socratic' else "",
        "style_custom": "selected" if config.get('PROMPT_STYLE') == 'custom' else "",
        "custom_style_display": "block" if config.get('PROMPT_STYLE') == 'custom' else "none",
        
        # Chat model settings
        "chat_model": config.get('CHAT_MODEL', 'gpt-3.5-turbo'),
        "chat_model_35": "selected" if config.get('CHAT_MODEL', 'gpt-3.5-turbo') == 'gpt-3.5-turbo' else "",
        "chat_model_4": "selected" if config.get('CHAT_MODEL') == 'gpt-4' else "",
        "chat_model_4t": "selected" if config.get('CHAT_MODEL') == 'gpt-4-turbo-preview' else "",
        "chat_max_tokens": config.get('CHAT_MAX_TOKENS', 1000),
        "chat_temperature": config.get('CHAT_TEMPERATURE', 0.7),
        "chat_presence_penalty": config.get('CHAT_PRESENCE_PENALTY', 0.1),
        "chat_frequency_penalty": config.get('CHAT_FREQUENCY_PENALTY', 0.1),
        
        # Memory settings
        "session_memory_limit": config.get('SESSION_MEMORY_CHAR_LIMIT', 15000),
        "persistent_memory_limit": config.get('PERSISTENT_MEMORY_CHAR_LIMIT', 8000),
        "max_prompt_chars": config.get('MAX_PROMPT_CHARS', 20000),
        "rag_context_limit": config.get('RAG_CONTEXT_CHAR_LIMIT', 4000),
        
        # Compression settings
        "compression_ratio": config.get('PERSISTENT_MEMORY_COMPRESSION_RATIO', 0.6),
        "comp_model_35": "selected" if config.get('PERSISTENT_MEMORY_COMPRESSION_MODEL', 'gpt-4') == 'gpt-3.5-turbo' else "",
        "comp_model_4": "selected" if config.get('PERSISTENT_MEMORY_COMPRESSION_MODEL', 'gpt-4') == 'gpt-4' else "",
        "min_compression_size": config.get('PERSISTENT_MEMORY_MIN_SIZE', 1000),
        "max_compressions": config.get('PERSISTENT_MEMORY_MAX_COMPRESSIONS', 3),
        "auto_summary_checked": "checked" if config.get('AUTO_SUMMARY_ENABLED', True) else "",
        "auto_compression_checked": "checked" if config.get('AUTO_COMPRESSION_ENABLED', True) else "",
        
        # Prompts
        "session_summary_prompt": config.get('SESSION_SUMMARY_PROMPT', ''),
        "compression_prompt": config.get('PERSISTENT_MEMORY_COMPRESSION_PROMPT', ''),
        
        # AI model settings
        "gpt_model": config.get('GPT_MODEL', 'gpt-4'),
        "gpt_model_35": "selected" if config.get('GPT_MODEL', 'gpt-4') == 'gpt-3.5-turbo' else "",
        "gpt_model_4": "selected" if config.get('GPT_MODEL', 'gpt-4') == 'gpt-4' else "",
        "summary_temperature": config.get('SUMMARY_TEMPERATURE', 0.3),
        
        # OpenAI defaults
        "openai_model": config.get('OPENAI_MODEL', 'gpt-3.5-turbo'),
        "openai_model_35": "selected" if config.get('OPENAI_MODEL', 'gpt-3.5-turbo') == 'gpt-3.5-turbo' else "",
        "openai_model_4": "selected" if config.get('OPENAI_MODEL') == 'gpt-4' else "",
        "openai_max_tokens": config.get('OPENAI_MAX_TOKENS', 2000),
        "openai_temperature": config.get('OPENAI_TEMPERATURE', 0.7),
        "openai_timeout": config.get('OPENAI_TIMEOUT', 30),
        "openai_top_p": config.get('OPENAI_TOP_P', 1.0),
        "openai_frequency_penalty": config.get('OPENAI_FREQUENCY_PENALTY', 0.0),
        "openai_presence_penalty": config.get('OPENAI_PRESENCE_PENALTY', 0.0),
    }
    
    return ADMIN_DASHBOARD_HTML.format(**template_vars)

@router.post("/admin")
async def save_admin_config(request: Request):
    """Save configuration from admin dashboard"""
    form_data = await request.form()
    
    # Update all configuration values
    for key, value in form_data.items():
        if key in ['AUTO_SUMMARY_ENABLED', 'AUTO_COMPRESSION_ENABLED']:
            # Handle checkboxes
            runtime_config.set_config(key, value == 'on')
        elif key in ['SESSION_MEMORY_CHAR_LIMIT', 'PERSISTENT_MEMORY_CHAR_LIMIT', 
                     'MAX_PROMPT_CHARS', 'RAG_CONTEXT_CHAR_LIMIT', 'TOP_K_RAG_HITS',
                     'CONVERSATION_HISTORY_LIMIT', 'CHAT_MAX_TOKENS', 'OPENAI_MAX_TOKENS',
                     'PERSISTENT_MEMORY_MIN_SIZE', 'PERSISTENT_MEMORY_MAX_COMPRESSIONS',
                     'OPENAI_TIMEOUT']:
            # Handle integers
            try:
                runtime_config.set_config(key, int(value))
            except ValueError:
                pass
        elif key in ['PERSISTENT_MEMORY_COMPRESSION_RATIO', 'CHAT_TEMPERATURE',
                     'CHAT_PRESENCE_PENALTY', 'CHAT_FREQUENCY_PENALTY',
                     'SUMMARY_TEMPERATURE', 'OPENAI_TEMPERATURE', 'OPENAI_TOP_P',
                     'OPENAI_FREQUENCY_PENALTY', 'OPENAI_PRESENCE_PENALTY']:
            # Handle floats
            try:
                runtime_config.set_config(key, float(value))
            except ValueError:
                pass
        else:
            # Handle strings
            runtime_config.set_config(key, value)
    
    # Redirect back with success message
    return RedirectResponse(url="/admin?success=true", status_code=302)

@router.get("/admin/reset")
async def reset_config():
    """Reset all configuration to defaults"""
    runtime_config.reset_to_defaults()
    return RedirectResponse(url="/admin?success=true", status_code=302)