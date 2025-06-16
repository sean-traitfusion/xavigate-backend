#!/bin/bash

# Test all conversation styles

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Testing All Conversation Styles${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"

# Check token
if [ -z "$COGNITO_TOKEN" ]; then
    echo -e "${RED}Error: No token provided${NC}"
    echo "Usage: export COGNITO_TOKEN='your-token'"
    exit 1
fi

# Base URLs
STORAGE_URL="http://localhost:8011"
CHAT_URL="http://localhost:8015"

# Test each style
for style in default empathetic analytical motivational socratic; do
    echo -e "\n${BLUE}Testing $style style...${NC}"
    
    # 1. Update config
    echo "Setting style to: $style"
    update_response=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$STORAGE_URL/api/memory/runtime-config" \
        -H "Authorization: Bearer $COGNITO_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "system_prompt": "You are Xavigate, an experienced Multiple Natures (MN) practitioner.",
            "conversation_history_limit": 5,
            "top_k_rag_hits": 5,
            "prompt_style": "'$style'",
            "temperature": 0.7,
            "max_tokens": 500
        }')
    
    http_code=$(echo "$update_response" | grep "HTTP_CODE:" | cut -d: -f2)
    if [ "$http_code" != "200" ]; then
        echo -e "${RED}Failed to update config (HTTP $http_code)${NC}"
        continue
    fi
    
    # 2. Make query
    echo "Making test query..."
    response=$(curl -s -X POST "$CHAT_URL/query" \
        -H "Authorization: Bearer $COGNITO_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "userId": "test-user",
            "username": "testuser",
            "fullName": "Test User",
            "sessionId": "test-'$style'-'$(date +%s)'",
            "traitScores": {"creative": 8.0, "conscientiousness": 3.0, "openness": 7.5},
            "message": "I struggle with procrastination and feel overwhelmed"
        }')
    
    # 3. Check response
    answer=$(echo "$response" | jq -r '.answer' 2>/dev/null)
    if [ -n "$answer" ] && [ "$answer" != "null" ]; then
        echo -e "${GREEN}✓ $style style successful${NC}"
        
        # Check for style indicators
        case $style in
            empathetic)
                if echo "$answer" | grep -iE "(feel|understand|hear you|challenging)" > /dev/null; then
                    echo -e "${GREEN}✓ Found empathetic language${NC}"
                fi
                ;;
            analytical)
                if echo "$answer" | grep -iE "([0-9]+\.|data|analysis|score)" > /dev/null; then
                    echo -e "${GREEN}✓ Found analytical language${NC}"
                fi
                ;;
            motivational)
                if echo "$answer" | grep -iE "(strength|potential|you can|power)" > /dev/null; then
                    echo -e "${GREEN}✓ Found motivational language${NC}"
                fi
                ;;
            socratic)
                if echo "$answer" | grep -E "\?" > /dev/null; then
                    echo -e "${GREEN}✓ Found questions${NC}"
                fi
                ;;
        esac
        
        echo "Response preview:"
        echo "$answer" | head -3
        echo "..."
    else
        echo -e "${RED}✗ Failed to get response${NC}"
    fi
    
    echo -e "${BLUE}────────────────────────────────────────────────────────────${NC}"
done

# Test custom style
echo -e "\n${BLUE}Testing custom style...${NC}"
curl -s -X POST "$STORAGE_URL/api/memory/runtime-config" \
    -H "Authorization: Bearer $COGNITO_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "system_prompt": "You are Xavigate, an MN practitioner.",
        "conversation_history_limit": 5,
        "top_k_rag_hits": 5,
        "prompt_style": "custom",
        "custom_style_modifier": "Respond like a wise Zen master - use metaphors and be contemplative",
        "temperature": 0.7,
        "max_tokens": 500
    }' > /dev/null

response=$(curl -s -X POST "$CHAT_URL/query" \
    -H "Authorization: Bearer $COGNITO_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "userId": "test-user",
        "username": "testuser",
        "fullName": "Test User",
        "sessionId": "test-custom-'$(date +%s)'",
        "traitScores": {"creative": 8.0, "conscientiousness": 3.0},
        "message": "How do I find balance?"
    }')

answer=$(echo "$response" | jq -r '.answer' 2>/dev/null)
if [ -n "$answer" ] && [ "$answer" != "null" ]; then
    echo -e "${GREEN}✓ Custom style successful${NC}"
    echo "Response preview:"
    echo "$answer" | head -3
fi

echo -e "\n${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Test Complete!${NC}"
echo ""
echo "Summary:"
echo "• Tested 5 preset styles + 1 custom style"
echo "• Each style should show distinct language patterns"
echo "• Empathetic: emotional validation"
echo "• Analytical: data and structure"
echo "• Motivational: encouragement and action"
echo "• Socratic: questions and reflection"
echo "• Custom: your defined style"