#!/usr/bin/env python3
"""
Simple configuration dashboard for the memory system
Based on Mobeus architecture but simplified for Xavigate
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
    <title>Memory System Configuration</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        .config-section {
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .config-item {
            margin: 15px 0;
        }
        label {
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
            color: #495057;
        }
        input, textarea, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 14px;
        }
        textarea {
            min-height: 120px;
            font-family: monospace;
        }
        .btn {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 5px;
        }
        .btn:hover {
            background-color: #0056b3;
        }
        .btn-danger {
            background-color: #dc3545;
        }
        .btn-danger:hover {
            background-color: #c82333;
        }
        .alert {
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-card {
            background: #e9ecef;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
        }
        .stat-label {
            font-size: 14px;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Memory System Configuration</h1>
        
        <div id="alert"></div>
        
        <div class="config-section">
            <h2>Memory Limits</h2>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value" id="session-limit">15,000</div>
                    <div class="stat-label">Session Memory Limit (chars)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="persistent-limit">8,000</div>
                    <div class="stat-label">Persistent Memory Limit (chars)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="prompt-limit">20,000</div>
                    <div class="stat-label">Max Prompt Size (chars)</div>
                </div>
            </div>
            
            <div class="config-item">
                <label for="session-memory-limit">Session Memory Character Limit:</label>
                <input type="number" id="session-memory-limit" name="SESSION_MEMORY_CHAR_LIMIT" value="15000">
            </div>
            
            <div class="config-item">
                <label for="persistent-memory-limit">Persistent Memory Character Limit:</label>
                <input type="number" id="persistent-memory-limit" name="PERSISTENT_MEMORY_CHAR_LIMIT" value="8000">
            </div>
            
            <div class="config-item">
                <label for="max-prompt-chars">Maximum Prompt Characters:</label>
                <input type="number" id="max-prompt-chars" name="MAX_PROMPT_CHARS" value="20000">
            </div>
        </div>
        
        <div class="config-section">
            <h2>Compression Settings</h2>
            <div class="config-item">
                <label for="compression-ratio">Compression Ratio (0.1 - 1.0):</label>
                <input type="number" id="compression-ratio" name="PERSISTENT_MEMORY_COMPRESSION_RATIO" 
                       value="0.6" min="0.1" max="1.0" step="0.1">
            </div>
            
            <div class="config-item">
                <label for="compression-model">Compression Model:</label>
                <select id="compression-model" name="PERSISTENT_MEMORY_COMPRESSION_MODEL">
                    <option value="gpt-4">GPT-4</option>
                    <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                </select>
            </div>
        </div>
        
        <div class="config-section">
            <h2>Feature Flags</h2>
            <div class="config-item">
                <label>
                    <input type="checkbox" id="auto-summary" name="AUTO_SUMMARY_ENABLED" checked>
                    Enable Auto-Summarization
                </label>
            </div>
            
            <div class="config-item">
                <label>
                    <input type="checkbox" id="auto-compression" name="AUTO_COMPRESSION_ENABLED" checked>
                    Enable Auto-Compression
                </label>
            </div>
            
            <div class="config-item">
                <label>
                    <input type="checkbox" id="voice-commands" name="VOICE_COMMAND_DETECTION_ENABLED" checked>
                    Enable Voice Command Detection
                </label>
            </div>
        </div>
        
        <div class="config-section">
            <h2>Prompts</h2>
            <div class="config-item">
                <label for="summary-prompt">Session Summary Prompt:</label>
                <textarea id="summary-prompt" name="SESSION_SUMMARY_PROMPT"></textarea>
            </div>
            
            <div class="config-item">
                <label for="compression-prompt">Compression Prompt:</label>
                <textarea id="compression-prompt" name="PERSISTENT_MEMORY_COMPRESSION_PROMPT"></textarea>
            </div>
        </div>
        
        <div class="config-section">
            <h2>Voice Command Triggers</h2>
            <div class="config-item">
                <label for="memory-triggers">Memory Triggers (comma-separated):</label>
                <input type="text" id="memory-triggers" name="MEMORY_TRIGGERS" 
                       value="remember this,store this,save this,don't forget,keep in mind,note that">
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <button class="btn" onclick="saveConfig()">💾 Save Configuration</button>
            <button class="btn btn-danger" onclick="resetDefaults()">🔄 Reset to Defaults</button>
        </div>
    </div>
    
    <script>
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
                    } else if (element.name === 'MEMORY_TRIGGERS') {
                        config[element.name] = element.value.split(',').map(s => s.trim());
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
            
            document.getElementById('session-limit').textContent = 
                parseInt(sessionLimit).toLocaleString();
            document.getElementById('persistent-limit').textContent = 
                parseInt(persistentLimit).toLocaleString();
            document.getElementById('prompt-limit').textContent = 
                parseInt(promptLimit).toLocaleString();
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
    print("🚀 Starting Memory Configuration Dashboard on http://localhost:5000")
    app.run(debug=True, port=5000)