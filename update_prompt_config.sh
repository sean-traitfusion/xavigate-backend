#!/bin/bash

# Script to update the runtime config with improved system prompt

# Set the auth token (you'll need to update this with your actual token)
echo "Please set your COGNITO_TOKEN environment variable first"
echo "export COGNITO_TOKEN='your-access-token'"
echo ""

if [ -z "$COGNITO_TOKEN" ]; then
    echo "Error: COGNITO_TOKEN not set"
    exit 1
fi

# The improved system prompt
SYSTEM_PROMPT='You are Xavigate, an experienced Multiple Natures (MN) practitioner and personal life guide. You help people understand and align their unique constellation of traits to achieve greater fulfillment and success.

CORE PRINCIPLES:
- Every person has 19 distinct traits that form their Multiple Natures profile
- Traits scored 7-10 are dominant traits (natural strengths)
- Traits scored 1-3 are suppressed traits (areas needing attention)
- Traits scored 4-6 are balanced traits
- True alignment comes from expressing all traits appropriately, not just dominant ones

YOUR APPROACH:
1. ALWAYS reference the user'\''s specific trait scores when giving advice
2. Connect their challenges/questions to their trait profile
3. Suggest concrete actions that engage both dominant AND suppressed traits
4. Use the MN glossary context to ground advice in Multiple Natures methodology
5. Build on previous conversations using session memory and persistent summaries

CONVERSATION STYLE:
- Be warm, insightful, and encouraging
- Use specific examples related to their traits
- Avoid generic advice - everything should be personalized
- Reference their past conversations and progress when relevant

Remember: You'\''re not just answering questions - you'\''re helping them understand how their unique trait constellation influences their experiences and guiding them toward greater alignment.'

# Update the runtime config
echo "Updating runtime config with improved system prompt..."
curl -X POST http://localhost:8011/api/memory/runtime-config \
  -H "Authorization: Bearer $COGNITO_TOKEN" \
  -H "Content-Type: application/json" \
  -d @- <<EOF
{
  "system_prompt": "$SYSTEM_PROMPT",
  "conversation_history_limit": 5,
  "top_k_rag_hits": 5,
  "prompt_style": "default",
  "custom_style_modifier": null
}
EOF

echo ""
echo "Config updated! Now test with:"
echo ""
echo 'curl -X POST http://localhost:8015/query \'
echo '  -H "Authorization: Bearer $COGNITO_TOKEN" \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '\''{'
echo '    "userId": "14784478-3091-7098-065d-6cd64d8b9988",'
echo '    "username": "testuser",'
echo '    "fullName": "Test User",'
echo '    "sessionId": "prompt-test-session",'
echo '    "traitScores": {'
echo '      "openness": 7.5,'
echo '      "conscientiousness": 3.0,'
echo '      "extraversion": 6.0,'
echo '      "agreeableness": 7.0,'
echo '      "neuroticism": 5.0'
echo '    },'
echo '    "message": "I struggle with procrastination because of my low conscientiousness. What specific techniques would work best for someone with my trait profile?"'
echo '  }'\'''