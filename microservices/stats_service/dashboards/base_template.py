def get_base_template(title: str, content: str, active_section: str = "config", user_info: dict = None) -> str:
    """Generate the base dashboard template with sidebar navigation."""
    # Show user info and logout button if authenticated
    user_section = ""
    if user_info:
        user_email = user_info.get('email', 'User')
        user_section = f"""
            <div class="user-section">
                <div class="user-info">
                    <svg class="user-icon" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/>
                    </svg>
                    <span class="user-email">{user_email}</span>
                </div>
                <a href="#" class="logout-link" data-route="/logout">
                    <svg class="logout-icon" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd"/>
                    </svg>
                    Logout
                </a>
            </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - Xavigate Dashboard</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #f5f5f7;
                color: #333;
                display: flex;
                min-height: 100vh;
            }}
            
            /* Sidebar Styles */
            .sidebar {{
                width: 250px;
                background: #1a1a2e;
                color: white;
                padding: 0;
                position: fixed;
                height: 100vh;
                overflow-y: auto;
                box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
            }}
            
            .sidebar-header {{
                padding: 2rem 1.5rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .sidebar-header h1 {{
                font-size: 1.5rem;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }}
            
            .sidebar-nav {{
                padding: 1rem 0;
            }}
            
            .nav-section {{
                margin-bottom: 2rem;
            }}
            
            .nav-section-title {{
                padding: 0.5rem 1.5rem;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: rgba(255, 255, 255, 0.5);
            }}
            
            .nav-link {{
                display: flex;
                align-items: center;
                padding: 0.75rem 1.5rem;
                color: rgba(255, 255, 255, 0.8);
                text-decoration: none;
                transition: all 0.2s;
                position: relative;
            }}
            
            .nav-link:hover {{
                background: rgba(255, 255, 255, 0.05);
                color: white;
            }}
            
            .nav-link.active {{
                background: rgba(102, 126, 234, 0.2);
                color: white;
            }}
            
            .nav-link.active::before {{
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 3px;
                background: #667eea;
            }}
            
            .nav-icon {{
                width: 20px;
                height: 20px;
                margin-right: 0.75rem;
                opacity: 0.8;
            }}
            
            /* Main Content Styles */
            .main-content {{
                flex: 1;
                margin-left: 250px;
                padding: 2rem;
                max-width: 1200px;
                width: 100%;
            }}
            
            .content-header {{
                margin-bottom: 2rem;
            }}
            
            .content-header h2 {{
                font-size: 2rem;
                font-weight: 600;
                color: #1a1a2e;
                margin-bottom: 0.5rem;
            }}
            
            .content-header p {{
                color: #666;
                font-size: 1.1rem;
            }}
            
            /* Card Styles */
            .card {{
                background: white;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
                margin-bottom: 2rem;
            }}
            
            .card h3 {{
                margin-top: 0;
                margin-bottom: 1.5rem;
                color: #1a1a2e;
                font-size: 1.25rem;
                font-weight: 600;
                border-bottom: 2px solid #f0f0f0;
                padding-bottom: 0.75rem;
            }}
            
            /* Responsive */
            @media (max-width: 768px) {{
                .sidebar {{
                    transform: translateX(-100%);
                    transition: transform 0.3s;
                }}
                
                .sidebar.open {{
                    transform: translateX(0);
                }}
                
                .main-content {{
                    margin-left: 0;
                    padding: 1rem;
                }}
            }}
            
            /* Additional Dashboard Styles */
            textarea {{
                width: 100%;
                min-height: 200px;
                font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
                padding: 1rem;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                resize: vertical;
                font-size: 0.9rem;
                background: #f9f9f9;
            }}
            
            input, select {{
                padding: 0.75rem 1rem;
                font-size: 1rem;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background: white;
                transition: border-color 0.2s;
            }}
            
            input:focus, select:focus, textarea:focus {{
                outline: none;
                border-color: #667eea;
            }}
            
            input[type="number"] {{
                width: 120px;
            }}
            
            input[type="range"] {{
                width: 100%;
                max-width: 400px;
            }}
            
            .range-container {{
                display: flex;
                align-items: center;
                gap: 1rem;
            }}
            
            .range-value {{
                font-weight: 600;
                min-width: 50px;
                color: #667eea;
            }}
            
            select {{
                width: 100%;
                max-width: 300px;
            }}
            
            button {{
                padding: 0.75rem 2rem;
                font-size: 1rem;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 500;
                transition: all 0.2s;
                margin-right: 1rem;
            }}
            
            button[value="save"] {{
                background: #667eea;
                color: white;
            }}
            
            button[value="save"]:hover {{
                background: #5a67d8;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }}
            
            button[value="test"] {{
                background: #48bb78;
                color: white;
            }}
            
            button[value="test"]:hover {{
                background: #38a169;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3);
            }}
            
            label {{
                display: block;
                margin-top: 1.5rem;
                margin-bottom: 0.5rem;
                font-weight: 600;
                color: #2d3748;
            }}
            
            .help-text {{
                font-size: 0.875rem;
                color: #718096;
                margin-top: 0.25rem;
                margin-bottom: 0.5rem;
            }}
            
            .grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 2rem;
            }}
            
            @media (max-width: 768px) {{
                .grid {{
                    grid-template-columns: 1fr;
                }}
            }}
            
            .status-message {{
                padding: 1rem;
                border-radius: 8px;
                margin-bottom: 1rem;
                font-weight: 500;
            }}
            
            .status-message.success {{
                background: #c6f6d5;
                color: #22543d;
                border: 1px solid #9ae6b4;
            }}
            
            .status-message.error {{
                background: #fed7d7;
                color: #742a2a;
                border: 1px solid #fc8181;
            }}
            
            /* User section styles */
            .user-section {{
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 1.5rem;
                background: rgba(0, 0, 0, 0.2);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .user-info {{
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 1rem;
                color: rgba(255, 255, 255, 0.9);
            }}
            
            .user-icon {{
                width: 24px;
                height: 24px;
                opacity: 0.8;
            }}
            
            .user-email {{
                font-size: 0.875rem;
                font-weight: 500;
            }}
            
            .logout-link {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
                color: rgba(255, 255, 255, 0.8);
                text-decoration: none;
                font-size: 0.875rem;
                padding: 0.5rem 1rem;
                margin: 0 -1rem;
                border-radius: 6px;
                transition: all 0.2s;
            }}
            
            .logout-link:hover {{
                background: rgba(255, 255, 255, 0.1);
                color: white;
            }}
            
            .logout-icon {{
                width: 18px;
                height: 18px;
            }}
        </style>
    </head>
    <body>
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1>🧭 Xavigate Admin</h1>
            </div>
            <nav class="sidebar-nav">
                <div class="nav-section">
                    <div class="nav-section-title">Configuration</div>
                    <a href="#" data-route="/" class="nav-link {"active" if active_section == "config" else ""}">
                        <svg class="nav-icon" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
                        </svg>
                        System Config
                    </a>
                </div>
                
                <div class="nav-section">
                    <div class="nav-section-title">Analytics</div>
                    <a href="#" data-route="/logging" class="nav-link {"active" if active_section == "logging" else ""}">
                        <svg class="nav-icon" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                        </svg>
                        Logging & Metrics
                    </a>
                    <a href="#" data-route="/usage" class="nav-link">
                        <svg class="nav-icon" viewBox="0 0 20 20" fill="currentColor">
                            <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/>
                        </svg>
                        Usage Stats
                    </a>
                </div>
                
                <div class="nav-section">
                    <div class="nav-section-title">System</div>
                    <a href="#" data-route="/health" class="nav-link">
                        <svg class="nav-icon" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
                        </svg>
                        Health Monitor
                    </a>
                </div>
            </nav>
            {user_section}
        </aside>
        
        <main class="main-content">
            {content}
        </main>
        
        <script>
            // Handle navigation for both local and production environments
            document.addEventListener('DOMContentLoaded', function() {{
                const isProduction = window.location.hostname !== 'localhost';
                const baseUrl = isProduction ? '/system-admin' : '/dashboard';
                
                // Update all nav links
                document.querySelectorAll('.nav-link').forEach(link => {{
                    const route = link.getAttribute('data-route');
                    const fullPath = baseUrl + route;
                    link.href = fullPath;
                }});
                
                // Update logout link
                const logoutLink = document.querySelector('.logout-link');
                if (logoutLink) {{
                    const route = logoutLink.getAttribute('data-route');
                    const fullPath = baseUrl + route;
                    logoutLink.href = fullPath;
                }}
                
                // Update form action if exists
                const form = document.querySelector('form');
                if (form && form.action.includes('/dashboard/')) {{
                    form.action = baseUrl + '/';
                }}
            }});
        </script>
    </body>
    </html>
    """