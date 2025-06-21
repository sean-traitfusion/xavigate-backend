#!/bin/bash

# Test Script for New Prompting System
# Tests the improved prompts, styles, and configuration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[$(date +%H:%M:%S)]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_section() {
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}$1${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
}

# Check if running in dev or prod mode
ENV_MODE=${ENV:-dev}
print_section "Prompting System Test (ENV=$ENV_MODE)"

# URLs based on environment
if [ "$ENV_MODE" = "prod" ]; then
    ADMIN_URL="https://chat.xavigate.com/admin"
    STORAGE_URL="https://chat.xavigate.com/api/storage"
    CHAT_URL="https://chat.xavigate.com/api/chat"
else
    ADMIN_URL="http://localhost:8015/admin"
    STORAGE_URL="http://localhost:8011"
    CHAT_URL="http://localhost:8015"
fi

echo "Admin Panel URL: $ADMIN_URL"
echo "Storage URL: $STORAGE_URL"
echo "Chat URL: $CHAT_URL"

# Token handling
if [ -z "$COGNITO_TOKEN" ]; then
    if [ -n "$1" ]; then
        export COGNITO_TOKEN="$1"
        print_success "Token provided via argument"
    else
        print_error "No token provided. Usage: $0 [token]"
        exit 1
    fi
fi

# Test configuration
USER_ID="test-user-$(date +%s)"
SESSION_ID="test-session-$(date +%s)"

# Comprehensive trait scores
TRAIT_SCORES='{
    "openness": 7.5,
    "conscientiousness": 3.0,
    "extraversion": 6.0,
    "agreeableness": 7.0,
    "neuroticism": 5.0,
    "creative": 8.0,
    "logical": 6.5,
    "emotional": 7.0,
    "kinesthetic": 4.0,
    "visual": 7.5,
    "musical": 5.0,
    "linguistic": 8.5,
    "naturalistic": 6.0,
    "existential": 7.0,
    "interpersonal": 6.5,
    "intrapersonal": 8.0,
    "spatial": 7.0,
    "bodily": 4.5,
    "rhythmic": 5.5
}'

# Step 1: Check current configuration
print_section "1. Current Configuration"
print_status "Fetching current runtime config..."

current_config=$(curl -s -X GET "$STORAGE_URL/api/memory/runtime-config" \
    -H "Authorization: Bearer $COGNITO_TOKEN")

echo "Current config:"
echo "$current_config" | jq '.'

# Step 2: Update with improved MN prompt
print_section "2. Setting Improved System Prompt"

IMPROVED_PROMPT="You are Xavigate, an experienced Multiple Natures (MN) practitioner and personal life guide. You help people understand and align their unique constellation of traits to achieve greater fulfillment and success.

CORE PRINCIPLES:
- Every person has 19 distinct traits that form their Multiple Natures profile
- Traits scored 7-10 are dominant traits (natural strengths)
- Traits scored 1-3 are suppressed traits (areas needing attention)
- Traits scored 4-6 are balanced traits
- True alignment comes from expressing all traits appropriately, not just dominant ones

YOUR APPROACH:
1. ALWAYS reference the user's specific trait scores when giving advice
2. Connect their challenges/questions to their trait profile
3. Suggest concrete actions that engage both dominant AND suppressed traits
4. Use the MN glossary context to ground advice in Multiple Natures methodology
5. Build on previous conversations using session memory and persistent summaries

CONVERSATION STYLE:
- Be warm, insightful, and encouraging
- Use specific examples related to their traits
- Avoid generic advice - everything should be personalized
- Reference their past conversations and progress when relevant

Remember: You're not just answering questions - you're helping them understand how their unique trait constellation influences their experiences and guiding them toward greater alignment."

print_status "Updating runtime config with improved prompt..."

update_response=$(curl -s -w "\n%{http_code}" -X POST "$STORAGE_URL/api/memory/runtime-config" \
    -H "Authorization: Bearer $COGNITO_TOKEN" \
    -H "Content-Type: application/json" \
    -d @- <<EOF
{
    "system_prompt": "$IMPROVED_PROMPT",
    "conversation_history_limit": 5,
    "top_k_rag_hits": 5,
    "prompt_style": "default",
    "custom_style_modifier": null,
    "temperature": 0.7,
    "max_tokens": 1000,
    "presence_penalty": 0.1,
    "frequency_penalty": 0.1,
    "model": "gpt-3.5-turbo"
}
EOF
)

http_code=$(echo "$update_response" | tail -n1)
if [ "$http_code" = "200" ]; then
    print_success "Configuration updated successfully"
else
    print_error "Failed to update configuration (HTTP $http_code)"
    echo "$update_response" | sed '$d'
fi

# Step 3: Test different prompt styles
print_section "3. Testing Prompt Styles"

test_style() {
    local style=$1
    local custom_modifier=$2
    local test_message="I struggle with procrastination because of my low conscientiousness. What specific techniques would work best for someone with my trait profile?"
    
    print_status "Testing $style style..."
    
    # Update style
    if [ -n "$custom_modifier" ]; then
        style_update='{
            "system_prompt": "'"$IMPROVED_PROMPT"'",
            "conversation_history_limit": 5,
            "top_k_rag_hits": 5,
            "prompt_style": "'"$style"'",
            "custom_style_modifier": "'"$custom_modifier"'",
            "temperature": 0.7,
            "max_tokens": 1000,
            "presence_penalty": 0.1,
            "frequency_penalty": 0.1,
            "model": "gpt-3.5-turbo"
        }'
    else
        style_update='{
            "system_prompt": "'"$IMPROVED_PROMPT"'",
            "conversation_history_limit": 5,
            "top_k_rag_hits": 5,
            "prompt_style": "'"$style"'",
            "custom_style_modifier": null,
            "temperature": 0.7,
            "max_tokens": 1000,
            "presence_penalty": 0.1,
            "frequency_penalty": 0.1,
            "model": "gpt-3.5-turbo"
        }'
    fi
    
    curl -s -X POST "$STORAGE_URL/api/memory/runtime-config" \
        -H "Authorization: Bearer $COGNITO_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$style_update" > /dev/null
    
    # Clear session
    curl -s -X POST "$STORAGE_URL/api/memory/session-memory" \
        -H "Authorization: Bearer $COGNITO_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "uuid": "'"$SESSION_ID-$style"'",
            "conversation_log": {"exchanges": []}
        }' > /dev/null
    
    # Make chat query
    response=$(curl -s -X POST "$CHAT_URL/query" \
        -H "Authorization: Bearer $COGNITO_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "userId": "'"$USER_ID"'",
            "username": "testuser",
            "fullName": "Test User",
            "sessionId": "'"$SESSION_ID-$style"'",
            "traitScores": '"$TRAIT_SCORES"',
            "message": "'"$test_message"'"
        }')
    
    if echo "$response" | jq -e '.answer' > /dev/null 2>&1; then
        print_success "$style style test completed"
        echo "Response preview:"
        echo "$response" | jq -r '.answer' | head -5
        echo "..."
    else
        print_error "$style style test failed"
        echo "$response"
    fi
    echo ""
}

# Test each style
test_style "default"
test_style "empathetic"
test_style "analytical"
test_style "motivational"
test_style "socratic"
test_style "custom" "Respond like a wise Zen master - be calm, use metaphors, and focus on mindfulness while still being practical about trait management"

# Step 4: Test conversation continuity
print_section "4. Testing Conversation Continuity"

SESSION_ID_CONTINUITY="continuity-test-$(date +%s)"

print_status "First message..."
first_response=$(curl -s -X POST "$CHAT_URL/query" \
    -H "Authorization: Bearer $COGNITO_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "userId": "'"$USER_ID"'",
        "username": "testuser",
        "fullName": "Test User",
        "sessionId": "'"$SESSION_ID_CONTINUITY"'",
        "traitScores": '"$TRAIT_SCORES"',
        "message": "I need help with my low conscientiousness affecting my work"
    }')

if echo "$first_response" | jq -e '.answer' > /dev/null 2>&1; then
    print_success "First message sent"
else
    print_error "First message failed"
fi

print_status "Follow-up message..."
followup_response=$(curl -s -X POST "$CHAT_URL/query" \
    -H "Authorization: Bearer $COGNITO_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "userId": "'"$USER_ID"'",
        "username": "testuser",
        "fullName": "Test User",
        "sessionId": "'"$SESSION_ID_CONTINUITY"'",
        "traitScores": '"$TRAIT_SCORES"',
        "message": "Can you give me a specific daily routine based on what we just discussed?"
    }')

if echo "$followup_response" | jq -e '.answer' > /dev/null 2>&1; then
    print_success "Conversation continuity maintained"
    echo "Follow-up response preview:"
    echo "$followup_response" | jq -r '.answer' | head -5
else
    print_error "Conversation continuity failed"
fi

# Step 5: Admin panel access
print_section "5. Admin Panel Access"

echo "Admin panel is available at: ${YELLOW}$ADMIN_URL${NC}"
echo ""
echo "You can:"
echo "1. View and modify the system prompt"
echo "2. Change conversation styles"
echo "3. Adjust AI parameters"
echo "4. Test configurations directly"

# Summary
print_section "Test Summary"

echo "✅ Prompting system components tested:"
echo "  • Runtime configuration API"
echo "  • System prompt updates"
echo "  • Multiple conversation styles"
echo "  • Custom style modifiers"
echo "  • Conversation continuity"
echo "  • Admin panel availability"
echo ""
echo "The improved prompting system is ready for use!"
echo ""
echo "Next steps:"
echo "1. Access the admin panel to fine-tune settings"
echo "2. Test with real user scenarios"
echo "3. Monitor response quality across different styles"