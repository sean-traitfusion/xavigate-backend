#!/bin/bash
# Final E2E Test Script for Xavigate

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Xavigate E2E Test (Final Version)${NC}"
echo "================================"

# Check if AUTH_TOKEN is set
if [ -z "$AUTH_TOKEN" ]; then
    echo -e "${RED}❌ Error: AUTH_TOKEN not set${NC}"
    echo "Please export your Cognito access token:"
    echo 'export AUTH_TOKEN="your-token-here"'
    exit 1
fi

echo -e "${GREEN}✓ AUTH_TOKEN is set${NC}"
echo "Token preview: ${AUTH_TOKEN:0:20}..."

# Function to test endpoint
test_endpoint() {
    local name="$1"
    local method="$2"
    local url="$3"
    local data="$4"
    
    echo -e "\n${YELLOW}Testing: $name${NC}"
    echo "URL: $url"
    
    if [ "$method" = "POST" ]; then
        if [ -n "$data" ]; then
            response=$(curl -s -w "\n%{http_code}" -X POST "$url" \
                -H "Content-Type: application/json" \
                -H "Authorization: Bearer $AUTH_TOKEN" \
                -d "$data" 2>&1)
        else
            response=$(curl -s -w "\n%{http_code}" -X POST "$url" \
                -H "Authorization: Bearer $AUTH_TOKEN" 2>&1)
        fi
    else
        response=$(curl -s -w "\n%{http_code}" -X GET "$url" \
            -H "Authorization: Bearer $AUTH_TOKEN" 2>&1)
    fi
    
    # Extract status code (last line)
    status_code=$(echo "$response" | tail -1)
    # Extract body (all but last line)
    body=$(echo "$response" | head -n -1)
    
    if [ "$status_code" = "200" ]; then
        echo -e "${GREEN}✅ Success (200)${NC}"
        echo "Response: $(echo "$body" | head -c 100)..."
        return 0
    else
        echo -e "${RED}❌ Failed (${status_code})${NC}"
        echo "Response: $body"
        return 1
    fi
}

# Initialize counters
total=0
passed=0

echo -e "\n${GREEN}Starting tests...${NC}"

# Test 1: Vector Search (no auth required)
echo -e "\n1️⃣ Vector Search Test"
if test_endpoint "Vector Search" "POST" "http://localhost:8017/search" '{"query":"alignment dynamics","top_k":3}'; then
    ((passed++))
fi
((total++))

# Test 2: Auth Verification
echo -e "\n2️⃣ Auth Token Verification"
if test_endpoint "Auth Verify" "POST" "http://localhost:8014/verify" "{\"key\":\"$AUTH_TOKEN\"}"; then
    ((passed++))
fi
((total++))

# Test 3: Memory Save
echo -e "\n3️⃣ Memory Save Test"
session_id="test-session-$(date +%s)"
if test_endpoint "Memory Save" "POST" "http://localhost:8011/api/memory/save" \
    "{\"userId\":\"test-user\",\"sessionId\":\"$session_id\",\"messages\":[{\"role\":\"user\",\"content\":\"Test message\"},{\"role\":\"assistant\",\"content\":\"Test response\"}]}"; then
    ((passed++))
fi
((total++))

# Test 4: Chat Query
echo -e "\n4️⃣ Chat Query Test"
if test_endpoint "Chat Query" "POST" "http://localhost:8015/query" \
    "{\"userId\":\"test-user\",\"username\":\"testuser\",\"fullName\":\"Test User\",\"sessionId\":\"$session_id\",\"message\":\"Hello, can you help me?\",\"traitScores\":{\"openness\":7.5,\"conscientiousness\":6.0,\"extraversion\":7.0,\"agreeableness\":8.0,\"neuroticism\":4.5}}"; then
    ((passed++))
fi
((total++))

# Test 5: Memory Retrieve
echo -e "\n5️⃣ Memory Retrieve Test"
if test_endpoint "Memory Get" "GET" "http://localhost:8011/api/memory/get/$session_id"; then
    ((passed++))
fi
((total++))

# Summary
echo -e "\n${GREEN}==============================${NC}"
echo -e "${GREEN}📊 TEST SUMMARY${NC}"
echo -e "${GREEN}==============================${NC}"
echo -e "Total: ${passed}/${total} tests passed"

if [ "$passed" -eq "$total" ]; then
    echo -e "${GREEN}✅ All tests passed! System is ready.${NC}"
else
    echo -e "${YELLOW}⚠️ Some tests failed.${NC}"
    echo -e "\nPossible issues:"
    echo "1. Token might be expired (tokens expire after 1 hour)"
    echo "2. Services need Cognito configuration in .env:"
    echo "   COGNITO_REGION=us-east-1"
    echo "   COGNITO_USER_POOL_ID=us-east-1_csH9tZFJF"
    echo "   COGNITO_APP_CLIENT_ID=56352i5933v40t36u1fqs2fe3e"
    echo "3. Services might need restart after adding config:"
    echo "   docker compose restart"
fi