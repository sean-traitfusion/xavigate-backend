// CognitoLogin.tsx - CORRECTED VERSION based on AWS sample
import React, { useEffect, useState } from 'react';

// ✅ CORRECTED CLIENT ID (fixed character: i not l)
const CLIENT_ID = "56352i5933v40t36u1fqs2fe3e";
const REDIRECT_URI = "http://localhost:3000/auth/callback";

// ✅ CORRECTED ENDPOINTS - Use custom domain for both authorize AND token
const AUTH_DOMAIN = "https://us-east-1csh9tzfjf.auth.us-east-1.amazoncognito.com";
const TOKEN_ENDPOINT = "https://us-east-1csh9tzfjf.auth.us-east-1.amazoncognito.com/oauth2/token";
const AUTHORIZE_ENDPOINT = "https://us-east-1csh9tzfjf.auth.us-east-1.amazoncognito.com/oauth2/authorize";

// For logout, use the custom domain (as shown in AWS sample)
const LOGOUT_DOMAIN = "https://us-east-1csh9tzfjf.auth.us-east-1.amazoncognito.com";

const SCOPE = "email openid phone";

function generateCodeVerifier(length: number = 128): string {
  const array = new Uint8Array(length);
  window.crypto.getRandomValues(array);
  return btoa(String.fromCharCode(...Array.from(array)))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

async function generateCodeChallenge(codeVerifier: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(codeVerifier);
  const digest = await crypto.subtle.digest("SHA-256", data);
  return btoa(String.fromCharCode(...Array.from(new Uint8Array(digest))))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

const CognitoLogin: React.FC = () => {
  const [idToken, setIdToken] = useState<string | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [userInfo, setUserInfo] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [debugInfo, setDebugInfo] = useState<string[]>([]);

  const addDebugInfo = (info: string) => {
    setDebugInfo(prev => [...prev, `${new Date().toLocaleTimeString()}: ${info}`]);
    console.log(info);
  };

  useEffect(() => {
    addDebugInfo("Component mounted, checking for auth code in URL");
    
    const url = new URL(window.location.href);
    const code = url.searchParams.get("code");
    const error = url.searchParams.get("error");
    const errorDescription = url.searchParams.get("error_description");

    if (error) {
      const errorMsg = `Authentication error: ${error}${errorDescription ? ` - ${errorDescription}` : ''}`;
      setError(errorMsg);
      addDebugInfo(errorMsg);
      return;
    }

    if (code) {
      addDebugInfo(`✅ Authorization code received: ${code.substring(0, 20)}...`);
      
      const storedVerifier = localStorage.getItem("pkce_verifier");
      
      if (!storedVerifier) {
        const errorMsg = "Code verifier not found. Please try logging in again.";
        setError(errorMsg);
        addDebugInfo(`❌ ${errorMsg}`);
        return;
      }

      addDebugInfo(`✅ Code verifier found: ${storedVerifier.substring(0, 20)}...`);
      
      // Exchange code for tokens
      const tokenData = new URLSearchParams({
        grant_type: "authorization_code",
        client_id: CLIENT_ID,
        redirect_uri: REDIRECT_URI,
        code: code,
        code_verifier: storedVerifier,
      });

      addDebugInfo(`🔄 Exchanging code for tokens at: ${TOKEN_ENDPOINT}`);
      addDebugInfo(`📤 Request body: ${tokenData.toString()}`);

      fetch(TOKEN_ENDPOINT, {
        method: "POST",
        headers: { 
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: tokenData.toString(),
      })
        .then(async (res) => {
          addDebugInfo(`📡 Token response status: ${res.status} ${res.statusText}`);
          addDebugInfo(`📡 Response headers: ${JSON.stringify(Array.from(res.headers.entries()))}`);
          
          const responseText = await res.text();
          addDebugInfo(`📡 Response body: ${responseText}`);
          
          if (!res.ok) {
            let errorData;
            try {
              errorData = JSON.parse(responseText);
            } catch {
              errorData = { error: 'parse_error', error_description: responseText };
            }
            throw new Error(`HTTP ${res.status}: ${errorData.error || 'unknown'} - ${errorData.error_description || responseText}`);
          }
          
          return JSON.parse(responseText);
        })
        .then((data) => {
          if (data.error) {
            throw new Error(`Token error: ${data.error} - ${data.error_description || ''}`);
          }
          
          addDebugInfo("✅ Tokens received successfully!");
          setIdToken(data.id_token);
          setAccessToken(data.access_token);
          setRefreshToken(data.refresh_token);
          
          // Decode user info from ID token
          if (data.id_token) {
            try {
              const payload = JSON.parse(atob(data.id_token.split('.')[1]));
              setUserInfo(payload);
              addDebugInfo(`✅ User info decoded: ${payload.email || payload.sub}`);
            } catch (e) {
              addDebugInfo(`⚠️ Could not decode ID token: ${e instanceof Error ? e.message : String(e)}`);
            }
          }
          
          localStorage.removeItem("pkce_verifier");
          
          // Clean up URL
          window.history.replaceState({}, document.title, window.location.pathname);
        })
        .catch((err) => {
          const errorMsg = `Token exchange failed: ${err.message}`;
          console.error(errorMsg, err);
          setError(errorMsg);
          addDebugInfo(`❌ ${errorMsg}`);
        });
    }
  }, []);

  const handleLogin = async () => {
    try {
      addDebugInfo("🚀 Initiating PKCE login flow...");
      
      const verifier = generateCodeVerifier();
      const challenge = await generateCodeChallenge(verifier);
      localStorage.setItem("pkce_verifier", verifier);

      addDebugInfo(`🔐 Generated PKCE verifier: ${verifier.substring(0, 20)}...`);
      addDebugInfo(`🔑 Generated PKCE challenge: ${challenge.substring(0, 20)}...`);

      const authParams = new URLSearchParams({
        response_type: "code",
        client_id: CLIENT_ID,
        redirect_uri: REDIRECT_URI,
        scope: SCOPE,
        code_challenge_method: "S256",
        code_challenge: challenge,
        state: "auth_state_" + Math.random().toString(36).substring(2)
      });

      const authUrl = `${AUTHORIZE_ENDPOINT}?${authParams.toString()}`;

      addDebugInfo(`🌐 Redirecting to: ${authUrl.substring(0, 100)}...`);
      addDebugInfo(`📋 Full auth URL logged to console`);
      console.log("Full authorization URL:", authUrl);
      
      // Redirect immediately
      window.location.href = authUrl;
      
    } catch (err) {
      const errorMsg =
        err && typeof err === "object" && "message" in err
          ? `Login initiation failed: ${(err as { message: string }).message}`
          : "Login initiation failed: Unknown error";
      console.error(errorMsg, err);
      setError(errorMsg);
      addDebugInfo(`❌ ${errorMsg}`);
    }
  };

  const handleLogout = () => {
    const logoutUrl = `${LOGOUT_DOMAIN}/logout?client_id=${CLIENT_ID}&logout_uri=${encodeURIComponent(window.location.origin)}`;
    addDebugInfo(`🚪 Logging out via: ${logoutUrl}`);
    
    // Clear local state
    setIdToken(null);
    setAccessToken(null);
    setRefreshToken(null);
    setUserInfo(null);
    setError(null);
    setDebugInfo([]);
    localStorage.removeItem("pkce_verifier");
    
    // Redirect to logout
    window.location.href = logoutUrl;
  };

  const clearError = () => {
    setError(null);
    setDebugInfo([]);
  };

  return (
    <div style={{ padding: '20px', fontFamily: '-apple-system, BlinkMacSystemFont, sans-serif' }}>
      <h2>🔐 AWS Cognito PKCE Authentication</h2>
      
      {error && (
        <div style={{ 
          color: '#d73027', 
          marginBottom: '20px', 
          padding: '15px', 
          border: '1px solid #d73027',
          borderRadius: '6px',
          backgroundColor: '#fdedec'
        }}>
          <strong>❌ Error:</strong> {error}
          <button 
            onClick={clearError}
            style={{ 
              marginLeft: '10px', 
              padding: '5px 10px',
              fontSize: '12px',
              backgroundColor: '#d73027',
              color: 'white',
              border: 'none',
              borderRadius: '3px',
              cursor: 'pointer'
            }}
          >
            Clear
          </button>
        </div>
      )}
      
      {idToken ? (
        <div>
          <div style={{ 
            color: '#27ae60', 
            marginBottom: '20px',
            padding: '15px',
            border: '1px solid #27ae60',
            borderRadius: '6px',
            backgroundColor: '#eafaf1'
          }}>
            <strong>✅ Authentication Successful!</strong>
            {userInfo && (
              <div style={{ marginTop: '10px', fontSize: '14px' }}>
                👤 Welcome: <strong>{userInfo.email || userInfo.preferred_username || userInfo.sub}</strong>
              </div>
            )}
          </div>

          <div style={{ marginBottom: '20px' }}>
            <button 
              onClick={handleLogout}
              style={{
                padding: '10px 20px',
                fontSize: '16px',
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer'
              }}
            >
              🚪 Sign Out
            </button>
          </div>

          <details style={{ marginBottom: '20px' }}>
            <summary style={{ cursor: 'pointer', marginBottom: '10px' }}>
              <strong>🎫 View Tokens</strong>
            </summary>
            
            {userInfo && (
              <div style={{ marginBottom: '15px' }}>
                <strong>👤 User Information:</strong>
                <pre style={{ 
                  fontSize: "12px",
                  backgroundColor: '#f8f9fa',
                  padding: '10px',
                  border: '1px solid #dee2e6',
                  borderRadius: '4px',
                  overflow: 'auto'
                }}>
                  {JSON.stringify(userInfo, null, 2)}
                </pre>
              </div>
            )}
            
            <div style={{ marginBottom: '15px' }}>
              <strong>🆔 ID Token:</strong>
              <pre style={{ 
                fontSize: "10px",
                backgroundColor: '#f8f9fa',
                padding: '10px',
                border: '1px solid #dee2e6',
                borderRadius: '4px',
                overflow: 'auto',
                maxHeight: '150px'
              }}>
                {idToken}
              </pre>
            </div>
            
            {accessToken && (
              <div style={{ marginBottom: '15px' }}>
                <strong>🔑 Access Token:</strong>
                <pre style={{ 
                  fontSize: "10px",
                  backgroundColor: '#f8f9fa',
                  padding: '10px',
                  border: '1px solid #dee2e6',
                  borderRadius: '4px',
                  overflow: 'auto',
                  maxHeight: '150px'
                }}>
                  {accessToken}
                </pre>
              </div>
            )}
            
            {refreshToken && (
              <div>
                <strong>🔄 Refresh Token:</strong>
                <pre style={{ 
                  fontSize: "10px",
                  backgroundColor: '#f8f9fa',
                  padding: '10px',
                  border: '1px solid #dee2e6',
                  borderRadius: '4px',
                  overflow: 'auto',
                  maxHeight: '150px'
                }}>
                  {refreshToken}
                </pre>
              </div>
            )}
          </details>
        </div>
      ) : (
        <div>
          <button 
            onClick={handleLogin}
            style={{
              padding: '12px 24px',
              fontSize: '16px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}
          >
            🚀 Sign In with Cognito
          </button>
          
          <div style={{ marginTop: '30px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '6px' }}>
            <h3>📋 Configuration Info:</h3>
            <div style={{ fontSize: '14px', lineHeight: '1.6' }}>
              <p><strong>Client ID:</strong> <code>{CLIENT_ID}</code></p>
              <p><strong>Redirect URI:</strong> <code>{REDIRECT_URI}</code></p>
              <p><strong>Authority:</strong> <code>https://cognito-idp.us-east-1.amazonaws.com/us-east-1_csH9tZFJF</code></p>
              <p><strong>Scopes:</strong> <code>{SCOPE}</code></p>
              <p><strong>Authorize Endpoint:</strong> <code>{AUTHORIZE_ENDPOINT}</code></p>
              <p><strong>Token Endpoint:</strong> <code>{TOKEN_ENDPOINT}</code></p>
              <p><strong>Logout Domain:</strong> <code>{LOGOUT_DOMAIN}</code></p>
            </div>
          </div>
        </div>
      )}

      {debugInfo.length > 0 && (
        <details style={{ marginTop: '30px' }}>
          <summary style={{ cursor: 'pointer', marginBottom: '10px' }}>
            <strong>🔍 Debug Information ({debugInfo.length} events)</strong>
          </summary>
          <div style={{ 
            backgroundColor: '#f8f9fa',
            border: '1px solid #dee2e6',
            borderRadius: '4px',
            padding: '10px',
            maxHeight: '400px',
            overflowY: 'auto',
            fontSize: '12px',
            fontFamily: 'monospace'
          }}>
            {debugInfo.map((info, index) => (
              <div key={index} style={{ marginBottom: '5px', paddingBottom: '5px', borderBottom: '1px solid #eee' }}>
                {info}
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  );
};

export default CognitoLogin;