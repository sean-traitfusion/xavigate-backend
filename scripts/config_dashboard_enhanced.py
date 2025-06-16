#!/usr/bin/env python3
"""
Enhanced configuration dashboard for the memory system
Includes all settings with tooltips and better organization
"""
from flask import Flask, render_template_string, request, jsonify
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'microservices', 'storage_service'))

from config import runtime_config

app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Xavigate Runtime Configuration</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
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
        .tab:hover {
            color: #0366d6;
        }
        .tab.active {
            color: #0366d6;
        }
        .tab.active::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            right: 0;
            height: 2px;
            background: #0366d6;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
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
        .section-icon {
            font-size: 1.25rem;
        }
        .form-group {
            margin-bottom: 1.5rem;
        }
        .form-group:last-child {
            margin-bottom: 0;
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
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
        }
        .tooltip-icon {
            width: 16px;
            height: 16px;
            background: #6a737d;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: bold;
        }
        .tooltip-text {
            visibility: hidden;
            width: 250px;
            background-color: #24292e;
            color: #fff;
            text-align: left;
            border-radius: 6px;
            padding: 0.75rem;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -125px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.875rem;
            font-weight: normal;
            line-height: 1.4;
        }
        .tooltip:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
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
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem;
            background: #f6f8fa;
            border-radius: 6px;
            cursor: pointer;
        }
        .checkbox-group:hover {
            background: #f0f2f5;
        }
        input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        .checkbox-label {
            flex: 1;
            font-weight: normal;
            margin-bottom: 0;
            cursor: pointer;
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
            min-width: 60px;
            text-align: center;
            font-weight: 600;
            color: #0366d6;
        }
        .button-group {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid #e1e4e8;
        }
        .btn {
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        .btn-primary {
            background: #0366d6;
            color: white;
        }
        .btn-primary:hover {
            background: #0256c7;
            box-shadow: 0 2px 8px rgba(3, 102, 214, 0.3);
        }
        .btn-secondary {
            background: #e1e4e8;
            color: #24292e;
        }
        .btn-secondary:hover {
            background: #d1d5da;
        }
        .btn-danger {
            background: #d73a49;
            color: white;
        }
        .btn-danger:hover {
            background: #cb2431;
            box-shadow: 0 2px 8px rgba(215, 58, 73, 0.3);
        }
        .alert {
            padding: 1rem 1.5rem;
            border-radius: 6px;
            margin-bottom: 1.5rem;
            display: none;
            animation: slideIn 0.3s ease-out;
        }
        @keyframes slideIn {
            from {
                transform: translateY(-10px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        .alert-success {
            background: #28a745;
            color: white;
        }
        .alert-error {
            background: #dc3545;
            color: white;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
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
        .info-box {
            background: #f0f9ff;
            border: 1px solid #c3ddfd;
            border-radius: 6px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            color: #1a56db;
            font-size: 0.875rem;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 Xavigate Runtime Configuration</h1>
    </div>
    
    <div class="container">
        <div id="alert"></div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="session-limit">15,000</div>
                <div class="stat-label">Session Memory (chars)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="persistent-limit">8,000</div>
                <div class="stat-label">Persistent Memory (chars)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="prompt-limit">20,000</div>
                <div class="stat-label">Max Prompt (chars)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="compression-ratio">60%</div>
                <div class="stat-label">Compression Target</div>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('memory')">Memory Settings</button>
            <button class="tab" onclick="showTab('prompts')">Prompts</button>
            <button class="tab" onclick="showTab('openai')">OpenAI Settings</button>
            <button class="tab" onclick="showTab('advanced')">Advanced</button>
        </div>
        
        <!-- Memory Settings Tab -->
        <div id="memory-tab" class="tab-content active">
            <div class="section">
                <h2><span class="section-icon">💾</span> Memory Limits</h2>
                
                <div class="info-box">
                    ℹ️ These settings control how much conversation history and user context can be stored.
                </div>
                
                <div class="grid-2">
                    <div class="form-group">
                        <label>
                            Session Memory Limit
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Maximum characters for current conversation. When 90% full, 
                                    auto-summarization triggers. Default: 15,000 chars (~3,750 tokens)
                                </span>
                            </span>
                        </label>
                        <input type="number" id="session-memory-limit" name="SESSION_MEMORY_CHAR_LIMIT" 
                               value="15000" min="5000" max="50000" step="1000">
                    </div>
                    
                    <div class="form-group">
                        <label>
                            Persistent Memory Limit
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Maximum characters for user's long-term summaries. Auto-compresses 
                                    at 90% capacity. Default: 8,000 chars (~2,000 tokens)
                                </span>
                            </span>
                        </label>
                        <input type="number" id="persistent-memory-limit" name="PERSISTENT_MEMORY_CHAR_LIMIT" 
                               value="8000" min="2000" max="20000" step="1000">
                    </div>
                    
                    <div class="form-group">
                        <label>
                            Maximum Prompt Size
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Total character limit for prompts sent to OpenAI. Includes system 
                                    prompt, memories, and context. Default: 20,000 chars (~5,000 tokens)
                                </span>
                            </span>
                        </label>
                        <input type="number" id="max-prompt-chars" name="MAX_PROMPT_CHARS" 
                               value="20000" min="10000" max="100000" step="1000">
                    </div>
                    
                    <div class="form-group">
                        <label>
                            RAG Context Limit
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Maximum characters reserved for RAG/vector search results. 
                                    Default: 4,000 chars (~1,000 tokens)
                                </span>
                            </span>
                        </label>
                        <input type="number" id="rag-context-limit" name="RAG_CONTEXT_CHAR_LIMIT" 
                               value="4000" min="1000" max="10000" step="500">
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2><span class="section-icon">🗜️</span> Compression Settings</h2>
                
                <div class="grid-2">
                    <div class="form-group">
                        <label>
                            Compression Ratio
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Target compression ratio. 0.6 means compress to 60% of original 
                                    size. Lower = more compression, higher = less compression.
                                </span>
                            </span>
                        </label>
                        <div class="range-group">
                            <input type="range" id="compression-ratio" name="PERSISTENT_MEMORY_COMPRESSION_RATIO" 
                                   value="0.6" min="0.3" max="0.9" step="0.1" 
                                   oninput="updateRangeValue('compression-ratio')">
                            <span class="range-value" id="compression-ratio-value">0.6</span>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            Compression Model
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    AI model used for compression. GPT-4 provides better quality 
                                    but is slower and more expensive.
                                </span>
                            </span>
                        </label>
                        <select id="compression-model" name="PERSISTENT_MEMORY_COMPRESSION_MODEL">
                            <option value="gpt-4">GPT-4 (Better quality)</option>
                            <option value="gpt-3.5-turbo">GPT-3.5 Turbo (Faster)</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            Minimum Compression Size
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Don't compress if memory is smaller than this. Prevents 
                                    over-compression of small memories. Default: 1,000 chars
                                </span>
                            </span>
                        </label>
                        <input type="number" id="min-compression-size" name="PERSISTENT_MEMORY_MIN_SIZE" 
                               value="1000" min="500" max="5000" step="100">
                    </div>
                    
                    <div class="form-group">
                        <label>
                            Max Compressions
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Maximum times to compress the same memory. Higher values 
                                    risk losing information. Default: 3
                                </span>
                            </span>
                        </label>
                        <input type="number" id="max-compressions" name="PERSISTENT_MEMORY_MAX_COMPRESSIONS" 
                               value="3" min="1" max="10" step="1">
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2><span class="section-icon">⚙️</span> Feature Flags</h2>
                
                <div class="checkbox-group">
                    <input type="checkbox" id="auto-summary" name="AUTO_SUMMARY_ENABLED" checked>
                    <label for="auto-summary" class="checkbox-label">
                        <strong>Enable Auto-Summarization</strong> - 
                        Automatically summarize conversations when session memory approaches limit
                    </label>
                </div>
                
                <div class="checkbox-group">
                    <input type="checkbox" id="auto-compression" name="AUTO_COMPRESSION_ENABLED" checked>
                    <label for="auto-compression" class="checkbox-label">
                        <strong>Enable Auto-Compression</strong> - 
                        Automatically compress persistent memory when it gets too large
                    </label>
                </div>
            </div>
        </div>
        
        <!-- Prompts Tab -->
        <div id="prompts-tab" class="tab-content">
            <div class="section">
                <h2><span class="section-icon">📝</span> System Prompts</h2>
                
                <div class="form-group">
                    <label>
                        Session Summary Prompt
                        <span class="tooltip">
                            <span class="tooltip-icon">?</span>
                            <span class="tooltip-text">
                                Template used when summarizing conversations. Use {conversation_text} 
                                as placeholder for the actual conversation.
                            </span>
                        </span>
                    </label>
                    <textarea id="summary-prompt" name="SESSION_SUMMARY_PROMPT"></textarea>
                </div>
                
                <div class="form-group">
                    <label>
                        Compression Prompt
                        <span class="tooltip">
                            <span class="tooltip-icon">?</span>
                            <span class="tooltip-text">
                                Template for compressing persistent memory. Use {current_summary} 
                                for the text to compress and {compression_ratio} for the target.
                            </span>
                        </span>
                    </label>
                    <textarea id="compression-prompt" name="PERSISTENT_MEMORY_COMPRESSION_PROMPT"></textarea>
                </div>
            </div>
        </div>
        
        <!-- OpenAI Settings Tab -->
        <div id="openai-tab" class="tab-content">
            <div class="section">
                <h2><span class="section-icon">🤖</span> OpenAI Configuration</h2>
                
                <div class="info-box">
                    ℹ️ These settings will be used for all OpenAI API calls. Configure carefully to balance quality, speed, and cost.
                </div>
                
                <div class="grid-2">
                    <div class="form-group">
                        <label>
                            Model
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    The OpenAI model to use for chat completions. GPT-4 is more 
                                    capable but slower and more expensive.
                                </span>
                            </span>
                        </label>
                        <select id="openai-model" name="OPENAI_MODEL">
                            <option value="gpt-4">GPT-4</option>
                            <option value="gpt-4-turbo-preview">GPT-4 Turbo</option>
                            <option value="gpt-3.5-turbo" selected>GPT-3.5 Turbo</option>
                            <option value="gpt-3.5-turbo-16k">GPT-3.5 Turbo 16K</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            Max Tokens
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Maximum tokens to generate in response. Higher values allow 
                                    longer responses but cost more. Default: 2000
                                </span>
                            </span>
                        </label>
                        <input type="number" id="max-tokens" name="OPENAI_MAX_TOKENS" 
                               value="2000" min="100" max="4000" step="100">
                    </div>
                    
                    <div class="form-group">
                        <label>
                            Temperature
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Controls randomness. 0 = deterministic, 2 = very random. 
                                    Default: 0.7 for balanced creativity
                                </span>
                            </span>
                        </label>
                        <div class="range-group">
                            <input type="range" id="temperature" name="OPENAI_TEMPERATURE" 
                                   value="0.7" min="0" max="2" step="0.1" 
                                   oninput="updateRangeValue('temperature')">
                            <span class="range-value" id="temperature-value">0.7</span>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            Top P
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Nucleus sampling. Consider tokens with top_p probability mass. 
                                    Alternative to temperature. Default: 1.0
                                </span>
                            </span>
                        </label>
                        <div class="range-group">
                            <input type="range" id="top-p" name="OPENAI_TOP_P" 
                                   value="1.0" min="0" max="1" step="0.05" 
                                   oninput="updateRangeValue('top-p')">
                            <span class="range-value" id="top-p-value">1.0</span>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            Frequency Penalty
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Reduces repetition of tokens based on frequency. -2.0 to 2.0. 
                                    Positive values decrease repetition. Default: 0
                                </span>
                            </span>
                        </label>
                        <div class="range-group">
                            <input type="range" id="frequency-penalty" name="OPENAI_FREQUENCY_PENALTY" 
                                   value="0" min="-2" max="2" step="0.1" 
                                   oninput="updateRangeValue('frequency-penalty')">
                            <span class="range-value" id="frequency-penalty-value">0</span>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            Presence Penalty
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Encourages new topics. -2.0 to 2.0. Positive values increase 
                                    likelihood of new topics. Default: 0
                                </span>
                            </span>
                        </label>
                        <div class="range-group">
                            <input type="range" id="presence-penalty" name="OPENAI_PRESENCE_PENALTY" 
                                   value="0" min="-2" max="2" step="0.1" 
                                   oninput="updateRangeValue('presence-penalty')">
                            <span class="range-value" id="presence-penalty-value">0</span>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            Timeout (seconds)
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Maximum time to wait for OpenAI response. Increase for 
                                    complex requests. Default: 30 seconds
                                </span>
                            </span>
                        </label>
                        <input type="number" id="timeout" name="OPENAI_TIMEOUT" 
                               value="30" min="10" max="300" step="5">
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2><span class="section-icon">💰</span> Cost Optimization</h2>
                
                <div class="grid-2">
                    <div class="form-group">
                        <label>
                            Summary Temperature
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Temperature for summarization. Lower = more consistent 
                                    summaries. Default: 0.3
                                </span>
                            </span>
                        </label>
                        <div class="range-group">
                            <input type="range" id="summary-temperature" name="SUMMARY_TEMPERATURE" 
                                   value="0.3" min="0" max="1" step="0.1" 
                                   oninput="updateRangeValue('summary-temperature')">
                            <span class="range-value" id="summary-temperature-value">0.3</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Advanced Tab -->
        <div id="advanced-tab" class="tab-content">
            <div class="section">
                <h2><span class="section-icon">🔧</span> Advanced Settings</h2>
                
                <div class="grid-2">
                    <div class="form-group">
                        <label>
                            GPT Model (General)
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Model for non-chat operations like summarization. Can be 
                                    different from chat model for cost optimization.
                                </span>
                            </span>
                        </label>
                        <select id="gpt-model" name="GPT_MODEL">
                            <option value="gpt-4" selected>GPT-4</option>
                            <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            General Temperature
                            <span class="tooltip">
                                <span class="tooltip-icon">?</span>
                                <span class="tooltip-text">
                                    Temperature for non-chat operations. Lower for consistency, 
                                    higher for creativity. Default: 0.7
                                </span>
                            </span>
                        </label>
                        <div class="range-group">
                            <input type="range" id="general-temperature" name="TEMPERATURE" 
                                   value="0.7" min="0" max="2" step="0.1" 
                                   oninput="updateRangeValue('general-temperature')">
                            <span class="range-value" id="general-temperature-value">0.7</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="button-group">
            <button class="btn btn-primary" onclick="saveConfig()">
                <span>💾</span> Save Configuration
            </button>
            <button class="btn btn-secondary" onclick="exportConfig()">
                <span>📥</span> Export Config
            </button>
            <button class="btn btn-danger" onclick="resetDefaults()">
                <span>🔄</span> Reset to Defaults
            </button>
        </div>
    </div>
    
    <script>
        // Tab management
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
        
        // Update range value display
        function updateRangeValue(id) {
            const range = document.getElementById(id);
            const value = document.getElementById(id + '-value');
            value.textContent = range.value;
        }
        
        // Load current configuration
        async function loadConfig() {
            try {
                const response = await fetch('/api/config');
                const config = await response.json();
                
                // Update form fields
                for (const [key, value] of Object.entries(config)) {
                    const element = document.querySelector(`[name="${key}"]`);
                    if (element) {
                        if (element.type === 'checkbox') {
                            element.checked = value;
                        } else if (Array.isArray(value)) {
                            element.value = value.join(',');
                        } else {
                            element.value = value;
                        }
                        
                        // Update range displays
                        if (element.type === 'range') {
                            const valueDisplay = document.getElementById(element.id + '-value');
                            if (valueDisplay) {
                                valueDisplay.textContent = value;
                            }
                        }
                    }
                }
                
                // Update stats display
                updateStats();
                
            } catch (error) {
                showAlert('Failed to load configuration: ' + error.message, 'error');
            }
        }
        
        // Save configuration
        async function saveConfig() {
            const config = {};
            
            // Collect all form inputs
            document.querySelectorAll('input, textarea, select').forEach(element => {
                if (element.name) {
                    if (element.type === 'checkbox') {
                        config[element.name] = element.checked;
                    } else if (element.type === 'number') {
                        config[element.name] = parseFloat(element.value);
                    } else if (element.type === 'range') {
                        config[element.name] = parseFloat(element.value);
                    } else {
                        config[element.name] = element.value;
                    }
                }
            });
            
            try {
                const response = await fetch('/api/config', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(config)
                });
                
                if (response.ok) {
                    showAlert('Configuration saved successfully!', 'success');
                    updateStats();
                } else {
                    throw new Error('Failed to save configuration');
                }
            } catch (error) {
                showAlert('Failed to save configuration: ' + error.message, 'error');
            }
        }
        
        // Export configuration
        function exportConfig() {
            const config = {};
            document.querySelectorAll('input, textarea, select').forEach(element => {
                if (element.name) {
                    if (element.type === 'checkbox') {
                        config[element.name] = element.checked;
                    } else if (element.type === 'number' || element.type === 'range') {
                        config[element.name] = parseFloat(element.value);
                    } else {
                        config[element.name] = element.value;
                    }
                }
            });
            
            const blob = new Blob([JSON.stringify(config, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'xavigate-config.json';
            a.click();
            URL.revokeObjectURL(url);
        }
        
        // Reset to defaults
        async function resetDefaults() {
            if (confirm('Are you sure you want to reset all settings to defaults?')) {
                try {
                    const response = await fetch('/api/reset', {method: 'POST'});
                    if (response.ok) {
                        showAlert('Configuration reset to defaults!', 'success');
                        loadConfig();
                    }
                } catch (error) {
                    showAlert('Failed to reset configuration: ' + error.message, 'error');
                }
            }
        }
        
        // Update statistics display
        function updateStats() {
            const sessionLimit = document.querySelector('[name="SESSION_MEMORY_CHAR_LIMIT"]').value;
            const persistentLimit = document.querySelector('[name="PERSISTENT_MEMORY_CHAR_LIMIT"]').value;
            const promptLimit = document.querySelector('[name="MAX_PROMPT_CHARS"]').value;
            const compressionRatio = document.querySelector('[name="PERSISTENT_MEMORY_COMPRESSION_RATIO"]').value;
            
            document.getElementById('session-limit').textContent = 
                parseInt(sessionLimit).toLocaleString();
            document.getElementById('persistent-limit').textContent = 
                parseInt(persistentLimit).toLocaleString();
            document.getElementById('prompt-limit').textContent = 
                parseInt(promptLimit).toLocaleString();
            document.getElementById('compression-ratio').textContent = 
                Math.round(compressionRatio * 100) + '%';
        }
        
        // Show alert message
        function showAlert(message, type) {
            const alertDiv = document.getElementById('alert');
            alertDiv.className = `alert alert-${type}`;
            alertDiv.textContent = message;
            alertDiv.style.display = 'block';
            
            setTimeout(() => {
                alertDiv.style.display = 'none';
            }, 5000);
        }
        
        // Initialize on load
        loadConfig();
        
        // Update range values on input
        document.querySelectorAll('input[type="range"]').forEach(range => {
            range.addEventListener('input', () => updateRangeValue(range.id));
        });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(runtime_config.all_config())

@app.route('/api/config', methods=['POST'])
def update_config():
    data = request.json
    for key, value in data.items():
        runtime_config.set_config(key, value)
    return jsonify({"status": "ok"})

@app.route('/api/reset', methods=['POST'])
def reset_config():
    runtime_config.reset_to_defaults()
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("🚀 Starting Xavigate Configuration Dashboard on http://localhost:5001")
    print("📝 Features:")
    print("   - Memory limits configuration")
    print("   - Compression settings")
    print("   - OpenAI parameters")
    print("   - Prompt templates")
    print("   - Export/import configuration")
    print("\n⚠️  Note: If port 5001 is in use, try a different port with: app.run(port=XXXX)")
    app.run(debug=True, port=5001, host='0.0.0.0')