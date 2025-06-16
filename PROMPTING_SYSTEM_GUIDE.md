# Xavigate Prompting System Guide

## Overview

The Xavigate prompting system uses runtime configuration to customize AI responses based on Multiple Natures (MN) methodology. It supports multiple conversation styles and can be configured through an admin panel.

## Key Features

1. **Runtime Configuration**: Modify prompts without restarting services
2. **Multiple Conversation Styles**: Default, Empathetic, Analytical, Motivational, Socratic, Custom
3. **MN Trait Integration**: Responses reference user's specific trait scores
4. **Admin Panel**: Web UI for real-time configuration at `/admin`

## Architecture

### Components

1. **Chat Service** (`microservices/chat_service/`)
   - `main.py`: Orchestrates chat requests
   - `prompt_builder.py`: Builds styled prompts with modifiers

2. **Storage Service** (`microservices/storage_service/`)
   - Runtime config API endpoints
   - Persistent storage for configuration

3. **Vector Service** (`microservices/vector_service/`)
   - RAG retrieval for MN glossary context

## Configuration

### Environment Setup

```bash
# Required environment variables
export OPENAI_API_KEY="your-openai-api-key"
export COGNITO_TOKEN="your-cognito-access-token"  # For production
```

### Docker Compose

The system runs in different modes:

```bash
# Development mode (no auth required)
docker-compose up

# Production mode (requires Cognito auth)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## Admin Panel Usage

### Access

- **Development**: http://localhost:8015/admin
- **Production**: https://chat.xavigate.com/admin

### Configuration Options

1. **System Prompt**: Main prompt defining Xavigate's behavior
2. **Conversation Style**: Choose from 6 options
3. **Model Parameters**:
   - Model selection (GPT-3.5, GPT-4)
   - Temperature (0-1)
   - Max tokens
   - Top K RAG hits
   - Presence/Frequency penalties

### Using the Admin Panel

1. Enter your Cognito token (production only)
2. Modify configuration as needed
3. Test with sample message
4. Save configuration

## Conversation Styles

### Default
- Warm, insightful MN practitioner
- Balanced approach

### Empathetic
- Starts with emotional validation
- Uses phrases like "I hear you", "That must be challenging"
- Focuses on emotional support before solutions

### Analytical
- Data-driven responses
- Numbered points and structure
- References specific trait scores and percentages

### Motivational
- Energetic, action-oriented
- Emphasizes strengths and potential
- Uses power words and exclamation points

### Socratic
- Guides through questions
- Encourages self-reflection
- Minimal direct advice

### Custom
- Define your own style modifier
- Complete flexibility in tone and approach

## Testing

### Basic Test
```bash
# Test all conversation styles
./test_prompting_styles_final.sh
```

### Production Test
```bash
# With authentication
export COGNITO_TOKEN="your-token"
./test_prompting_system.sh
```

## API Examples

### Update Configuration
```bash
curl -X POST http://localhost:8011/api/memory/runtime-config \
  -H "Authorization: Bearer $COGNITO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "system_prompt": "Your custom prompt",
    "prompt_style": "empathetic",
    "temperature": 0.8
  }'
```

### Make Chat Query
```bash
curl -X POST http://localhost:8015/query \
  -H "Authorization: Bearer $COGNITO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "user-123",
    "username": "testuser",
    "sessionId": "session-123",
    "traitScores": {
      "openness": 7.5,
      "conscientiousness": 3.0,
      "creative": 8.0
    },
    "message": "How can I be more organized?"
  }'
```

## Troubleshooting

### Service Won't Start
- Check for syntax errors: `docker logs xavigate_chat_service`
- Verify OPENAI_API_KEY is set

### Authentication Issues
- Ensure using access token (not ID token)
- Check token hasn't expired
- Verify ENV=prod in docker-compose

### Responses Not Styled
- Verify style is saved in config
- Check prompt_builder.py has style modifiers
- Test with admin panel

### Hanging Requests
- Check OpenAI API connectivity
- Verify token is valid
- Check service logs for errors

## Production Deployment

1. Use production docker-compose:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

2. Set environment variables:
   ```bash
   export ENV=prod
   export OPENAI_API_KEY="..."
   export POSTGRES_PASSWORD="..."
   ```

3. Access via nginx routing:
   - Admin: https://chat.xavigate.com/admin
   - API: https://chat.xavigate.com/api/chat/query

## Next Steps

1. The config dashboard will be moved to stats_service
2. A main dashboard with sidebar navigation is planned
3. Additional dashboards for conversation analytics coming soon