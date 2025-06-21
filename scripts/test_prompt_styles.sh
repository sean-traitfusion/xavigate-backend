#!/bin/bash

# Test script for different prompt styles

if [ -z "$COGNITO_TOKEN" ]; then
    echo "Error: COGNITO_TOKEN not set"
    echo "Please run: export COGNITO_TOKEN='your-access-token'"
    exit 1
fi

# Base system prompt
BASE_PROMPT='You are Xavigate, an experienced Multiple Natures (MN) practitioner and personal life guide. You help people understand and align their unique constellation of traits to achieve greater fulfillment and success.

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

# Test question
TEST_MESSAGE="I struggle with procrastination because of my low conscientiousness. What specific techniques would work best for someone with my trait profile?"

echo "Testing Different Prompt Styles"
echo "=============================="
echo ""

# Function to test a style
test_style() {
    local style=$1
    local custom_modifier=$2
    
    echo "Testing $style style..."
    echo "------------------------"
    
    # Update config with style
    curl -s -X POST http://localhost:8011/api/memory/runtime-config \
      -H "Authorization: Bearer $COGNITO_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"system_prompt\": \"$BASE_PROMPT\",
        \"conversation_history_limit\": 5,
        \"top_k_rag_hits\": 5,
        \"prompt_style\": \"$style\",
        \"custom_style_modifier\": $custom_modifier
      }" > /dev/null
    
    # Clear session for fresh test
    curl -s -X POST http://localhost:8011/api/memory/session-memory \
      -H "Authorization: Bearer $COGNITO_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "uuid": "style-test-session",
        "conversation_log": {"exchanges": []}
      }' > /dev/null
    
    # Make query
    response=$(curl -s -X POST http://localhost:8015/query \
      -H "Authorization: Bearer $COGNITO_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "userId": "14784478-3091-7098-065d-6cd64d8b9988",
        "username": "testuser",
        "fullName": "Test User",
        "sessionId": "style-test-session",
        "traitScores": {
          "openness": 7.5,
          "conscientiousness": 3.0,
          "extraversion": 6.0,
          "agreeableness": 7.0,
          "neuroticism": 5.0,
          "creative": 8.0,
          "logical": 6.5,
          "emotional": 7.0,
          "kinesthetic": 4.0,
          "visual": 7.5
        },
        "message": "'"$TEST_MESSAGE"'"
      }')
    
    # Extract and display answer
    answer=$(echo "$response" | jq -r '.answer // "No answer received"')
    echo "$answer" | fold -s -w 80
    echo ""
    echo ""
}

# Test each style
test_style "default" "null"
test_style "empathetic" "null"
test_style "analytical" "null"
test_style "motivational" "null"
test_style "socratic" "null"

# Test custom style
echo "Testing custom style (Dave Chappelle voice)..."
echo "------------------------"
test_style "custom" '"Respond in the voice of Dave Chappelle - use humor, be real and direct, throw in some comedy while still being helpful. Keep it authentic and conversational."'

echo "All tests complete!"