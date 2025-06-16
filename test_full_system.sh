#!/bin/bash
set -e

TOKEN="eyJraWQiOiJlbW5HZmZ2elZcL3VWeEQwQ1cxQitkdEpBXC9RXC9aMmlqdXJcLzRvZmdrTmhyYz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIxNDc4NDQ3OC0zMDkxLTcwOTgtMDY1ZC02Y2Q2NGQ4Yjk5ODgiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9jc0g5dFpGSkYiLCJ2ZXJzaW9uIjoyLCJjbGllbnRfaWQiOiI1NjM1Mmk1OTMzdjQwdDM2dTFmcXMyZmUzZSIsIm9yaWdpbl9qdGkiOiI5Nzg0MzY0NC03ZDdmLTRiYWQtOGI3OS04NDcxOWVlYWE4MTAiLCJldmVudF9pZCI6ImYzZDMxNzRjLWUyMzItNGZkZS1hZTZmLTIwMWFlMzM0ZjNjMyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoicGhvbmUgb3BlbmlkIGVtYWlsIiwiYXV0aF90aW1lIjoxNzUwMDM5MzA3LCJleHAiOjE3NTAwNDI5MDcsImlhdCI6MTc1MDAzOTMwNywianRpIjoiZWNhYzIzYjgtNDJmMS00YjBmLWI1ZTAtNzdiZGRlZmYyZGQ3IiwidXNlcm5hbWUiOiIxNDc4NDQ3OC0zMDkxLTcwOTgtMDY1ZC02Y2Q2NGQ4Yjk5ODgifQ.gXjK3GR1ATw-aBe3uUYT__q6iSIM8sS919OTnZfQz_jr6OLzqu_OSnOZ1N9n-WZgb1HpLN86FSGjJsZdgpViO6fGfiMClJKPyZH2qbiS_anDANif6hSVki7wBOazZ5H7EWok3PVNPxMkHoBQaHLVfzPHkwMmqiHYpGB8Uqbl0GP8WCiCaVy6irtjgi3RJJzkcwvvU_GEpUV4bjforja6bvYc2Qi7_t2iJNysbbcj99y0QezX2e85BIiGfvK3ugyRuxpNA9wOTTmHRHBegRnMQd0zqr-WF6qqQU_VoGnVsszUkLlcVvnLS9UgAhBOS3i6MWK8XmxPpV4BfdEOF9bHmA"
USER_ID="14784478-3091-7098-065d-6cd64d8b9988"
SESSION_ID="prod-test-comprehensive-$(date +%s)"

echo "🚀 Comprehensive Xavigate System Test"
echo "====================================="
echo "Session ID: $SESSION_ID"
echo

# 1. Test memory save
echo "1️⃣ Testing memory save..."
curl -s -w "\nHTTP Status: %{http_code}\n" \
  -X POST http://localhost:8011/api/memory/save \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"userId\": \"$USER_ID\",
    \"sessionId\": \"$SESSION_ID\",
    \"messages\": [
      {\"role\": \"user\", \"content\": \"I have low conscientiousness and struggle with procrastination\"},
      {\"role\": \"assistant\", \"content\": \"I understand you struggle with procrastination due to low conscientiousness. Let's work on strategies.\"}
    ]
  }"

# 2. Test memory retrieval
echo -e "\n2️⃣ Testing memory retrieval..."
curl -s -X GET "http://localhost:8011/api/memory/get/$SESSION_ID" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

# 3. Test chat with context
echo -e "\n3️⃣ Testing chat service with memory context..."
RESPONSE=$(curl -s -X POST http://localhost:8015/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"userId\": \"$USER_ID\",
    \"username\": \"testuser\",
    \"fullName\": \"Test User\",
    \"sessionId\": \"$SESSION_ID\",
    \"traitScores\": {
      \"openness\": 7.5,
      \"conscientiousness\": 3.0,
      \"extraversion\": 6.0,
      \"agreeableness\": 7.0,
      \"neuroticism\": 5.0
    },
    \"message\": \"Based on our previous discussion about my low conscientiousness, what's the single most effective technique I should start with today?\"
  }")

echo "$RESPONSE" | jq -r '.answer' 2>/dev/null || echo "$RESPONSE"

# 4. Test memory stats
echo -e "\n\n4️⃣ Testing memory statistics..."
curl -s -X GET "http://localhost:8011/api/memory/memory-stats/$USER_ID" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

# 5. Test runtime config
echo -e "\n5️⃣ Testing runtime configuration..."
curl -s -X GET http://localhost:8011/api/memory/runtime-config \
  -H "Authorization: Bearer $TOKEN" | jq '.'

echo -e "\n✅ Test complete!"