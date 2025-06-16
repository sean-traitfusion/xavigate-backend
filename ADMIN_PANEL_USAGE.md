# Admin Panel Usage Guide

## Access the Admin Panel

1. **URL**: http://localhost:8015/admin
2. **First Time Setup**:
   - Enter your Cognito access token in the "Auth Token" field
   - When you click outside the field (blur event), it will automatically load your current configuration
   - You'll see an alert saying "Configuration loaded successfully!"

## Using the Admin Panel

### 1. System Prompt
- This is the main prompt that defines how Xavigate behaves
- The default prompt includes comprehensive MN methodology guidance
- You can modify it to adjust the AI's behavior

### 2. Conversation Style
- **Default**: Warm & insightful MN practitioner
- **Empathetic**: Focuses on emotional validation
- **Analytical**: Data-driven responses
- **Motivational**: Action-oriented coaching
- **Socratic**: Question-based discovery
- **Custom**: Define your own style in the text area below

### 3. Model Parameters
- **Top K RAG Hits**: Number of knowledge base results (1-10)
- **Model**: Choose GPT-3.5 Turbo, GPT-4, or GPT-4 Turbo
- **Temperature**: 0 = focused, 1 = creative
- **Max Tokens**: Response length limit
- **Presence Penalty**: Encourages topic diversity
- **Frequency Penalty**: Reduces repetition

### 4. Testing
1. Make your configuration changes
2. Enter a test message
3. Click "Test Configuration" to see how the AI responds

### 5. Saving
- Click "Save Configuration" to persist your changes
- Changes take effect immediately
- No service restart needed

## Troubleshooting

### "Failed to load configuration"
- Make sure your token is valid
- Token should be an access token (not ID token)
- Try refreshing the page and re-entering the token

### Changes not taking effect
- Ensure you clicked "Save Configuration"
- Check that you got a success message
- Try testing with a new session ID

### Database errors resolved
- The PostgreSQL index syntax errors have been fixed
- Tables will be created properly on service restart

## Quick Test

After making changes, test with:

```bash
export COGNITO_TOKEN='your-token'
./test_prompting_system.sh
```

Or manually:

```bash
curl -X POST http://localhost:8015/query \
  -H "Authorization: Bearer $COGNITO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "test-user",
    "username": "testuser",
    "fullName": "Test User",
    "sessionId": "test-session",
    "traitScores": {
      "conscientiousness": 3.0,
      "creative": 8.0,
      "logical": 6.5
    },
    "message": "How can I be more organized?"
  }'
```