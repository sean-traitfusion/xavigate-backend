def get_logging_dashboard_content() -> str:
    """Generate the logging dashboard content with full chat pipeline visibility."""
    return """
        <div class="content-header">
            <h2>Chat Pipeline Logging</h2>
            <p>Monitor prompts, responses, and performance metrics</p>
        </div>
        
        
        <!-- Filters Section -->
        <div class="card">
            <h3>Filters</h3>
            <div class="form-grid">
                <div class="form-group">
                    <label>User ID</label>
                    <input type="text" id="filter-user-id" placeholder="Filter by user ID">
                </div>
                <div class="form-group">
                    <label>Date Range</label>
                    <input type="date" id="filter-date-start">
                    <input type="date" id="filter-date-end" style="margin-top: 0.5rem;">
                </div>
                <div class="form-group">
                    <label>Search Text</label>
                    <input type="text" id="filter-search" placeholder="Search in messages">
                </div>
                <div class="form-group">
                    <label>Model</label>
                    <select id="filter-model">
                        <option value="">All Models</option>
                        <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                        <option value="gpt-4">GPT-4</option>
                        <option value="gpt-4-turbo">GPT-4 Turbo</option>
                    </select>
                </div>
            </div>
            <div style="margin-top: 1rem;">
                <button class="primary" onclick="loadLogs()">Apply Filters</button>
                <button onclick="clearFilters()">Clear</button>
            </div>
        </div>

        <!-- Statistics Overview -->
        <div class="card">
            <h3>Statistics</h3>
            <div id="stats-container" class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value" id="total-interactions">-</div>
                    <div class="stat-label">Total Interactions</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="avg-response-time">-</div>
                    <div class="stat-label">Avg Response Time</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="error-rate">-</div>
                    <div class="stat-label">Error Rate</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="active-users">-</div>
                    <div class="stat-label">Active Users</div>
                </div>
            </div>
        </div>

        <!-- Logs Table -->
        <div class="card">
            <h3>Recent Interactions</h3>
            <div id="logs-container">
                <div class="loading">Loading logs...</div>
            </div>
            <div style="margin-top: 1rem; text-align: center;">
                <button id="load-more" onclick="loadMore()" style="display: none;">Load More</button>
            </div>
        </div>

        <!-- Detailed View Modal -->
        <div id="detail-modal" class="modal" style="display: none;">
            <div class="modal-content">
                <span class="close" onclick="closeModal()">&times;</span>
                <h2>Interaction Details</h2>
                <div id="modal-body"></div>
            </div>
        </div>

        <style>
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-top: 1rem;
            }
            
            .stat-item {
                text-align: center;
                padding: 1.5rem;
                background: #f8f9fa;
                border-radius: 8px;
            }
            
            .stat-value {
                font-size: 2rem;
                font-weight: 600;
                color: #2c3e50;
            }
            
            .stat-label {
                color: #666;
                margin-top: 0.5rem;
            }
            
            .log-entry {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1rem;
                background: #fff;
                cursor: pointer;
                transition: all 0.2s;
            }
            
            .log-entry:hover {
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                transform: translateY(-1px);
            }
            
            .log-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.5rem;
            }
            
            .log-timestamp {
                color: #666;
                font-size: 0.9rem;
            }
            
            .log-model {
                background: #e3f2fd;
                color: #1976d2;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                font-size: 0.85rem;
            }
            
            .log-user-message {
                background: #f5f5f5;
                padding: 0.75rem;
                border-radius: 4px;
                margin: 0.5rem 0;
            }
            
            .log-assistant-response {
                background: #e8f5e9;
                padding: 0.75rem;
                border-radius: 4px;
                margin: 0.5rem 0;
            }
            
            .log-metrics {
                display: flex;
                gap: 1rem;
                margin-top: 0.5rem;
                font-size: 0.85rem;
                color: #666;
            }
            
            .metric-item {
                display: flex;
                align-items: center;
                gap: 0.25rem;
            }
            
            .error-indicator {
                background: #ffebee;
                color: #c62828;
                padding: 0.5rem;
                border-radius: 4px;
                margin-top: 0.5rem;
            }
            
            .modal {
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.5);
            }
            
            .modal-content {
                background-color: #fefefe;
                margin: 5% auto;
                padding: 20px;
                border: 1px solid #888;
                width: 80%;
                max-width: 900px;
                max-height: 80vh;
                overflow-y: auto;
                border-radius: 8px;
            }
            
            .close {
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
                cursor: pointer;
            }
            
            .close:hover {
                color: black;
            }
            
            .detail-section {
                margin: 1.5rem 0;
            }
            
            .detail-section h3 {
                margin-bottom: 0.5rem;
                color: #2c3e50;
            }
            
            .code-block {
                background: #f5f5f5;
                padding: 1rem;
                border-radius: 4px;
                overflow-x: auto;
                font-family: monospace;
                font-size: 0.85rem;
                white-space: pre-wrap;
            }
            
            .loading {
                text-align: center;
                color: #666;
                padding: 2rem;
            }
        </style>

        <script>
            let currentOffset = 0;
            const limit = 20;
            let allLogs = [];
            
            // Use direct URL in development, proxied URL in production
            const baseUrl = window.location.hostname === 'localhost' 
                ? 'http://localhost:8011' 
                : '/api/storage';
            
            
            async function loadLogs() {
                const logsContainer = document.getElementById('logs-container');
                logsContainer.innerHTML = '<div class="loading">Loading logs...</div>';
                
                try {
                    const response = await fetch(baseUrl + '/logging/all-interactions?limit=' + limit + '&offset=0');
                    
                    if (!response.ok) {
                        const errorText = await response.text();
                        console.error('API Error:', response.status, errorText);
                        throw new Error(`Failed to fetch logs: ${response.status} ${response.statusText}`);
                    }
                    
                    const data = await response.json();
                    allLogs = data.interactions;
                    currentOffset = limit;
                    
                    // Apply client-side filters
                    const filteredLogs = applyFilters(allLogs);
                    displayLogs(filteredLogs);
                    updateStats(data);
                    
                    document.getElementById('load-more').style.display = 
                        data.total > limit ? 'inline-block' : 'none';
                } catch (error) {
                    console.error('Failed to load logs:', error);
                    logsContainer.innerHTML = 
                        '<div class="error-indicator">Failed to load logs: ' + error.message + '</div>';
                }
            }
            
            function applyFilters(logs) {
                const userId = document.getElementById('filter-user-id').value.toLowerCase();
                const dateStart = document.getElementById('filter-date-start').value;
                const dateEnd = document.getElementById('filter-date-end').value;
                const searchText = document.getElementById('filter-search').value.toLowerCase();
                const model = document.getElementById('filter-model').value;
                
                return logs.filter(log => {
                    // User ID filter
                    if (userId && !log.user_id.toLowerCase().includes(userId)) {
                        return false;
                    }
                    
                    // Date range filter
                    const logDate = new Date(log.timestamp);
                    if (dateStart && logDate < new Date(dateStart)) {
                        return false;
                    }
                    if (dateEnd && logDate > new Date(dateEnd + 'T23:59:59')) {
                        return false;
                    }
                    
                    // Search text filter
                    if (searchText) {
                        const searchInLog = 
                            log.user_message.toLowerCase().includes(searchText) ||
                            log.assistant_response.toLowerCase().includes(searchText);
                        if (!searchInLog) {
                            return false;
                        }
                    }
                    
                    // Model filter
                    if (model && log.model !== model) {
                        return false;
                    }
                    
                    return true;
                });
            }
            
            function displayLogs(logs) {
                const logsContainer = document.getElementById('logs-container');
                
                if (logs.length === 0) {
                    logsContainer.innerHTML = '<p style="text-align: center; color: #666;">No logs found</p>';
                    return;
                }
                
                logsContainer.innerHTML = logs.map(log => {
                    const timestamp = new Date(log.timestamp).toLocaleString();
                    const responseTime = log.metrics?.total_ms || 'N/A';
                    const truncatedResponse = log.assistant_response.length > 150 
                        ? log.assistant_response.substring(0, 150) + '...' 
                        : log.assistant_response;
                    
                    return `
                        <div class="log-entry" onclick="showDetails('${log.interaction_id}')">
                            <div class="log-header">
                                <span class="log-timestamp">${timestamp}</span>
                                <span class="log-model">${log.model}</span>
                            </div>
                            <div class="log-user-message">
                                <strong>User:</strong> ${escapeHtml(log.user_message)}
                            </div>
                            <div class="log-assistant-response">
                                <strong>Assistant:</strong> ${escapeHtml(truncatedResponse)}
                            </div>
                            <div class="log-metrics">
                                <div class="metric-item">
                                    <span>⏱️</span>
                                    <span>${responseTime}ms</span>
                                </div>
                                <div class="metric-item">
                                    <span>👤</span>
                                    <span>${log.user_id.substring(0, 8)}...</span>
                                </div>
                                ${log.error ? '<div class="error-indicator">Error: ' + log.error + '</div>' : ''}
                            </div>
                        </div>
                    `;
                }).join('');
            }
            
            function updateStats(data) {
                // Calculate statistics
                const totalInteractions = data.total || 0;
                let totalResponseTime = 0;
                let responseCount = 0;
                let errorCount = 0;
                const uniqueUsers = new Set();
                
                data.interactions.forEach(log => {
                    if (log.metrics?.total_ms) {
                        totalResponseTime += log.metrics.total_ms;
                        responseCount++;
                    }
                    if (log.error) {
                        errorCount++;
                    }
                    uniqueUsers.add(log.user_id);
                });
                
                const avgResponseTime = responseCount > 0 
                    ? Math.round(totalResponseTime / responseCount) 
                    : 0;
                const errorRate = totalInteractions > 0 
                    ? ((errorCount / totalInteractions) * 100).toFixed(1) 
                    : 0;
                
                // Update UI
                document.getElementById('total-interactions').textContent = totalInteractions;
                document.getElementById('avg-response-time').textContent = avgResponseTime + 'ms';
                document.getElementById('error-rate').textContent = errorRate + '%';
                document.getElementById('active-users').textContent = uniqueUsers.size;
            }
            
            async function loadMore() {
                try {
                    const response = await fetch(baseUrl + '/logging/all-interactions?limit=' + limit + '&offset=' + currentOffset);
                    
                    if (!response.ok) {
                        throw new Error('Failed to fetch more logs');
                    }
                    
                    const data = await response.json();
                    allLogs = allLogs.concat(data.interactions);
                    currentOffset += limit;
                    
                    // Apply filters to all logs
                    const filteredLogs = applyFilters(allLogs);
                    displayLogs(filteredLogs);
                    
                    if (currentOffset >= data.total) {
                        document.getElementById('load-more').style.display = 'none';
                    }
                } catch (error) {
                    alert('Failed to load more logs: ' + error.message);
                }
            }
            
            function showDetails(interactionId) {
                const log = allLogs.find(l => l.interaction_id === interactionId);
                if (!log) return;
                
                const modalBody = document.getElementById('modal-body');
                modalBody.innerHTML = `
                    <div class="detail-section">
                        <h3>Basic Information</h3>
                        <p><strong>Timestamp:</strong> ${new Date(log.timestamp).toLocaleString()}</p>
                        <p><strong>User ID:</strong> ${log.user_id}</p>
                        <p><strong>Interaction ID:</strong> ${log.interaction_id}</p>
                        <p><strong>Model:</strong> ${log.model}</p>
                    </div>
                    
                    <div class="detail-section">
                        <h3>User Message</h3>
                        <div class="code-block">${escapeHtml(log.user_message)}</div>
                    </div>
                    
                    <div class="detail-section">
                        <h3>Assistant Response</h3>
                        <div class="code-block">${escapeHtml(log.assistant_response)}</div>
                    </div>
                    
                    <div class="detail-section">
                        <h3>RAG Context</h3>
                        <div class="code-block">${escapeHtml(log.rag_context || 'No RAG context')}</div>
                    </div>
                    
                    <div class="detail-section">
                        <h3>Performance Metrics</h3>
                        <p><strong>Total Time:</strong> ${log.metrics?.total_ms || 'N/A'}ms</p>
                        <p><strong>Memory Fetch:</strong> ${log.metrics?.memory_fetch_ms || 'N/A'}ms</p>
                        <p><strong>RAG Fetch:</strong> ${log.metrics?.rag_fetch_ms || 'N/A'}ms</p>
                        <p><strong>LLM Call:</strong> ${log.metrics?.llm_call_ms || 'N/A'}ms</p>
                    </div>
                    
                    ${log.error ? `
                        <div class="detail-section">
                            <h3>Error</h3>
                            <div class="error-indicator">${log.error}</div>
                        </div>
                    ` : ''}
                    
                    <div style="margin-top: 2rem;">
                        <button class="primary" onclick="loadPromptDetails('${log.user_id}', '${log.timestamp}')">
                            View Full Prompt Details
                        </button>
                    </div>
                `;
                
                document.getElementById('detail-modal').style.display = 'block';
            }
            
            async function loadPromptDetails(userId, timestamp) {
                try {
                    console.log(`Loading prompt details for user: ${userId}, timestamp: ${timestamp}`);
                    const response = await fetch(baseUrl + '/logging/prompts/' + userId + '?limit=10');
                    
                    if (!response.ok) {
                        throw new Error('Failed to fetch prompt details: ' + response.statusText);
                    }
                    
                    const data = await response.json();
                    console.log(`Found ${data.prompts.length} prompts for user`);
                    
                    // Find prompt with closest timestamp
                    const targetTime = new Date(timestamp).getTime();
                    let closestPrompt = null;
                    let closestDiff = Infinity;
                    
                    data.prompts.forEach(p => {
                        const promptTime = new Date(p.timestamp).getTime();
                        const diff = Math.abs(promptTime - targetTime);
                        if (diff < closestDiff && diff < 10000) { // Within 10 seconds
                            closestDiff = diff;
                            closestPrompt = p;
                        }
                    });
                    
                    if (closestPrompt) {
                        console.log('Found matching prompt');
                        const modalBody = document.getElementById('modal-body');
                        modalBody.innerHTML += `
                            <div class="detail-section">
                                <h3>System Prompt</h3>
                                <div class="code-block">${escapeHtml(closestPrompt.system_prompt)}</div>
                            </div>
                            
                            <div class="detail-section">
                                <h3>Persistent Memory</h3>
                                <div class="code-block">${escapeHtml(closestPrompt.persistent_summary || 'None')}</div>
                            </div>
                            
                            <div class="detail-section">
                                <h3>Session Context</h3>
                                <div class="code-block">${escapeHtml(closestPrompt.session_context || 'None')}</div>
                            </div>
                            
                            <div class="detail-section">
                                <h3>Final Prompt</h3>
                                <div class="code-block">${escapeHtml(closestPrompt.final_prompt)}</div>
                                <p style="margin-top: 0.5rem; color: #666;">
                                    Length: ${closestPrompt.prompt_length} chars | 
                                    Estimated tokens: ${closestPrompt.estimated_tokens}
                                </p>
                            </div>
                        `;
                    } else {
                        console.log('No matching prompt found within time window');
                        const modalBody = document.getElementById('modal-body');
                        modalBody.innerHTML += `
                            <div class="detail-section">
                                <p style="color: #666;">No prompt details found for this interaction.</p>
                            </div>
                        `;
                    }
                } catch (error) {
                    console.error('Failed to load prompt details:', error);
                    const modalBody = document.getElementById('modal-body');
                    modalBody.innerHTML += `
                        <div class="detail-section">
                            <p style="color: #c62828;">Error loading prompt details: ${error.message}</p>
                        </div>
                    `;
                }
            }
            
            function closeModal() {
                document.getElementById('detail-modal').style.display = 'none';
            }
            
            function clearFilters() {
                document.getElementById('filter-user-id').value = '';
                document.getElementById('filter-date-start').value = '';
                document.getElementById('filter-date-end').value = '';
                document.getElementById('filter-search').value = '';
                document.getElementById('filter-model').value = '';
                loadLogs();
            }
            
            function escapeHtml(text) {
                const map = {
                    '&': '&amp;',
                    '<': '&lt;',
                    '>': '&gt;',
                    '"': '&quot;',
                    "'": '&#039;'
                };
                return text.replace(/[&<>"']/g, m => map[m]);
            }
            
            // Close modal when clicking outside
            window.onclick = function(event) {
                const modal = document.getElementById('detail-modal');
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
            }
            
            // Load logs on page load
            loadLogs();
            
            // Refresh logs every 30 seconds
            setInterval(loadLogs, 30000);
        </script>
    """