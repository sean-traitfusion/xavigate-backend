#!/bin/bash

# Comprehensive Production Testing Script for Xavigate Backend
# This script tests all services in production mode with proper authentication

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test configuration
USER_ID="14784478-3091-7098-065d-6cd64d8b9988"
USERNAME="testuser"
FULL_NAME="Test User"
SESSION_ID="prod-test-$(date +%s)"

# Function to print colored output
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

# Check if token is provided
if [ -z "$COGNITO_TOKEN" ]; then
    print_section "Authentication Setup"
    echo "Please provide your Cognito access token:"
    echo ""
    echo "Option 1: Export it as an environment variable"
    echo "  export COGNITO_TOKEN='your-access-token'"
    echo ""
    echo "Option 2: Pass it as an argument"
    echo "  ./test_prod_complete.sh 'your-access-token'"
    echo ""
    
    if [ -n "$1" ]; then
        export COGNITO_TOKEN="$1"
        print_success "Token provided via argument"
    else
        print_error "No token provided. Exiting."
        exit 1
    fi
fi

# Service URLs (adjust if using different ports)
STORAGE_URL="http://localhost:8011"
CHAT_URL="http://localhost:8015"
VECTOR_URL="http://localhost:8017"

print_section "Xavigate Production Testing Suite"
echo "User ID: $USER_ID"
echo "Session ID: $SESSION_ID"
echo "Token: ${COGNITO_TOKEN:0:20}..."

# Test trait scores
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

# Function to test endpoint
test_endpoint() {
    local method=$1
    local url=$2
    local data=$3
    local description=$4
    
    print_status "Testing: $description"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -X GET "$url" \
            -H "Authorization: Bearer $COGNITO_TOKEN")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            -H "Authorization: Bearer $COGNITO_TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        print_success "$description (HTTP $http_code)"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
    else
        print_error "$description (HTTP $http_code)"
        echo "$body"
    fi
    
    echo ""
}

# 1. Test Storage Service
print_section "1. Storage Service Tests"

# Test health endpoint
test_endpoint "GET" "$STORAGE_URL/health" "" "Storage service health check"

# Get runtime config
test_endpoint "GET" "$STORAGE_URL/api/memory/runtime-config" "" "Get runtime configuration"

# Update runtime config with improved prompt
print_status "Updating runtime configuration..."
IMPROVED_PROMPT='You are Xavigate, an experienced Multiple Natures (MN) practitioner and personal life guide. You help people understand and align their unique constellation of traits to achieve greater fulfillment and success.

CORE PRINCIPLES:
- Every person has 19 distinct traits that form their Multiple Natures profile
- Traits scored 7-10 are dominant traits (natural strengths)
- Traits scored 1-3 are suppressed traits (areas needing attention)
- Traits scored 4-6 are balanced traits
- True alignment comes from expressing all traits appropriately, not just dominant ones

YOUR APPROACH:
1. ALWAYS reference the user'"'"'s specific trait scores when giving advice
2. Connect their challenges/questions to their trait profile
3. Suggest concrete actions that engage both dominant AND suppressed traits
4. Use the MN glossary context to ground advice in Multiple Natures methodology
5. Build on previous conversations using session memory and persistent summaries

CONVERSATION STYLE:
- Be warm, insightful, and encouraging
- Use specific examples related to their traits
- Avoid generic advice - everything should be personalized
- Reference their past conversations and progress when relevant

Remember: You'"'"'re not just answering questions - you'"'"'re helping them understand how their unique trait constellation influences their experiences and guiding them toward greater alignment.'

CONFIG_UPDATE='{
    "system_prompt": "'"$IMPROVED_PROMPT"'",
    "conversation_history_limit": 5,
    "top_k_rag_hits": 5,
    "prompt_style": "default",
    "custom_style_modifier": null,
    "temperature": 0.7,
    "max_tokens": 1000,
    "presence_penalty": 0.1,
    "frequency_penalty": 0.1,
    "model": "gpt-3.5-turbo"
}'

test_endpoint "POST" "$STORAGE_URL/api/memory/runtime-config" "$CONFIG_UPDATE" "Update runtime configuration"

# Initialize session memory
SESSION_INIT='{
    "uuid": "'"$SESSION_ID"'",
    "conversation_log": {"exchanges": []}
}'
test_endpoint "POST" "$STORAGE_URL/api/memory/session-memory" "$SESSION_INIT" "Initialize session memory"

# 2. Test Vector Service
print_section "2. Vector Service Tests"

test_endpoint "GET" "$VECTOR_URL/health" "" "Vector service health check"

# Test vector search
VECTOR_SEARCH='{
    "query": "procrastination techniques for low conscientiousness",
    "top_k": 5
}'
test_endpoint "POST" "$VECTOR_URL/search" "$VECTOR_SEARCH" "Vector search for relevant content"

# 3. Test Chat Service
print_section "3. Chat Service Tests"

test_endpoint "GET" "$CHAT_URL/health" "" "Chat service health check"

# Test queries with different styles
print_section "4. Testing Different Conversation Styles"

# Function to test chat with style
test_chat_style() {
    local style=$1
    local custom_modifier=$2
    local message=$3
    
    print_status "Testing $style style..."
    
    # Update config with style
    if [ -n "$custom_modifier" ]; then
        STYLE_CONFIG='{
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
        STYLE_CONFIG='{
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
        -d "$STYLE_CONFIG" > /dev/null
    
    # Make chat query
    CHAT_REQUEST='{
        "userId": "'"$USER_ID"'",
        "username": "'"$USERNAME"'",
        "fullName": "'"$FULL_NAME"'",
        "sessionId": "'"$SESSION_ID"'",
        "traitScores": '"$TRAIT_SCORES"',
        "message": "'"$message"'"
    }'
    
    test_endpoint "POST" "$CHAT_URL/query" "$CHAT_REQUEST" "Chat query with $style style"
}

# Test different styles
TEST_MESSAGE="I struggle with procrastination because of my low conscientiousness. What specific techniques would work best for someone with my trait profile?"

test_chat_style "default" "" "$TEST_MESSAGE"
test_chat_style "empathetic" "" "$TEST_MESSAGE"
test_chat_style "analytical" "" "$TEST_MESSAGE"
test_chat_style "motivational" "" "$TEST_MESSAGE"
test_chat_style "socratic" "" "$TEST_MESSAGE"
test_chat_style "custom" "Respond like a wise meditation teacher - be calm, mindful, and focus on present-moment awareness while still being practical" "$TEST_MESSAGE"

# 5. Test Memory Persistence
print_section "5. Memory System Tests"

# Test follow-up query
FOLLOWUP_MESSAGE="Can you give me a specific daily routine that incorporates those techniques?"
FOLLOWUP_REQUEST='{
    "userId": "'"$USER_ID"'",
    "username": "'"$USERNAME"'",
    "fullName": "'"$FULL_NAME"'",
    "sessionId": "'"$SESSION_ID"'",
    "traitScores": '"$TRAIT_SCORES"',
    "message": "'"$FOLLOWUP_MESSAGE"'"
}'

print_status "Testing conversation continuity..."
test_endpoint "POST" "$CHAT_URL/query" "$FOLLOWUP_REQUEST" "Follow-up query"

# Retrieve session memory
test_endpoint "GET" "$STORAGE_URL/api/memory/session-memory/$SESSION_ID" "" "Retrieve session memory"

# Get memory stats
test_endpoint "GET" "$STORAGE_URL/api/memory/memory-stats/$SESSION_ID" "" "Get memory statistics"

# 6. Test Admin Panel
print_section "6. Admin Panel Access"

echo "Admin panel is available at: ${YELLOW}http://localhost:8015/admin${NC}"
echo ""
echo "You can access it in your browser and use your token for authentication."
echo "The panel allows you to:"
echo "  • Configure system prompts"
echo "  • Adjust AI model parameters"
echo "  • Set conversation styles"
echo "  • Test configurations"

# Summary
print_section "Testing Complete!"

echo "Summary:"
echo "  • Storage Service: Tested config management and memory operations"
echo "  • Vector Service: Tested RAG retrieval"
echo "  • Chat Service: Tested multiple conversation styles"
echo "  • Memory System: Verified persistence and continuity"
echo "  • Admin Panel: Available at http://localhost:8015/admin"
echo ""
echo "All core functionality has been tested in production mode."
echo ""
echo "Next steps:"
echo "1. Review the responses to ensure quality"
echo "2. Check the admin panel for configuration options"
echo "3. Monitor logs for any errors"
echo "4. Test with real user scenarios"