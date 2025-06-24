def get_login_page_content(error_message: str = None) -> str:
    """Generate the login page content."""
    
    error_html = ""
    if error_message:
        error_html = f'<div class="error-message">{error_message}</div>'
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login - Xavigate Admin</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 1rem;
            }}
            
            .login-container {{
                background: white;
                padding: 3rem;
                border-radius: 16px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                width: 100%;
                max-width: 400px;
                text-align: center;
            }}
            
            .logo {{
                font-size: 3rem;
                margin-bottom: 1rem;
            }}
            
            h1 {{
                color: #1a1a2e;
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }}
            
            .subtitle {{
                color: #666;
                font-size: 1.1rem;
                margin-bottom: 2rem;
            }}
            
            .login-button {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.75rem;
                background: #667eea;
                color: white;
                padding: 1rem 2rem;
                font-size: 1.1rem;
                font-weight: 600;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                text-decoration: none;
                transition: all 0.2s;
                width: 100%;
            }}
            
            .login-button:hover {{
                background: #5a67d8;
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
            }}
            
            .login-button svg {{
                width: 24px;
                height: 24px;
            }}
            
            .error-message {{
                background: #fed7d7;
                color: #742a2a;
                padding: 1rem;
                border-radius: 8px;
                margin-bottom: 1.5rem;
                border: 1px solid #fc8181;
            }}
            
            .info-box {{
                background: #e6f7ff;
                border: 1px solid #91d5ff;
                color: #0050b3;
                padding: 1rem;
                border-radius: 8px;
                margin-top: 2rem;
                font-size: 0.9rem;
                text-align: left;
            }}
            
            .info-box strong {{
                display: block;
                margin-bottom: 0.5rem;
            }}
            
            .security-note {{
                margin-top: 2rem;
                color: #666;
                font-size: 0.875rem;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
            }}
            
            .security-note svg {{
                width: 16px;
                height: 16px;
                fill: #666;
            }}
            
            .loading {{
                display: none;
                color: #667eea;
                margin-top: 1rem;
            }}
            
            .loading.show {{
                display: block;
            }}
            
            @keyframes spin {{
                to {{ transform: rotate(360deg); }}
            }}
            
            .spinner {{
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 0.5rem;
            }}
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">🧭</div>
            <h1>Xavigate Admin</h1>
            <p class="subtitle">Sign in to access the admin panel</p>
            
            {error_html}
            
            <a href="#" class="login-button" onclick="handleLogin(); return false;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                    <polyline points="10 17 15 12 10 7"></polyline>
                    <line x1="15" y1="12" x2="3" y2="12"></line>
                </svg>
                Sign in with AWS Cognito
            </a>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                Redirecting to sign in...
            </div>
            
            <div class="info-box">
                <strong>Admin Access Required</strong>
                You must have valid admin credentials to access this panel. If you don't have access, please contact your system administrator.
            </div>
            
            <div class="security-note">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
                </svg>
                Secured with AWS Cognito
            </div>
        </div>
        
        <script>
            function handleLogin() {{
                document.getElementById('loading').classList.add('show');
                // Redirect to the auth endpoint which will handle the Cognito flow
                window.location.href = '{"/system-admin/auth/login" if error_message and "production" in error_message else "/dashboard/auth/login"}';
            }}
            
            // Check if we're coming back from a failed auth
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.has('error')) {{
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-message';
                errorDiv.textContent = 'Authentication failed: ' + urlParams.get('error_description') || urlParams.get('error');
                document.querySelector('.subtitle').after(errorDiv);
            }}
        </script>
    </body>
    </html>
    """