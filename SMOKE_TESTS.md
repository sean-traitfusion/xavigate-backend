# Xavigate Backend MVP Smoke Test Checklist

This checklist guides you through verifying core backend functionality end-to-end. Use `curl`, `httpie`, or Postman to exercise each endpoint. Assumes services are running locally via `docker-compose up --build`.

## Prerequisites
- Ensure Docker containers are up and healthy:
  ```sh
  docker-compose up --build -d
  ```
- Confirm each service’s Swagger UI is reachable:
  - Auth:    http://localhost:8014/docs
  - RAG:     http://localhost:8010/docs
  - Vector:  http://localhost:8017/docs
  - Storage: http://localhost:8011/docs
  - Chat:    http://localhost:8015/docs
  - MNTest:  http://localhost:8016/docs

---

## 1. Auth Service
1. **Health check**
   ```sh
   curl -s http://localhost:8014/health
   # Expected: {"status":"ok","service":"auth"}
   ```
2. **Verify stub** (dev mode always valid)
   ```sh
   curl -X POST http://localhost:8014/verify \
        -H "Content-Type: application/json" \
        -d '{"key":"foo"}'
   # Expected: {"valid":true,"sub":null}
   ```

## 2. MNTest Service
1. **Submit MN scores**
   ```sh
   curl -X POST http://localhost:8016/mntest/submit \
        -H "Content-Type: application/json" \
        -H "Content-Type: application/json" \
        -d '{
            "userId": "user123",
            "traitScores": {"creative": 8.4, "logical": 6.1, "administrative": 3.2}
        }'
   # Expected: {"status":"ok"}
   ```
2. **Retrieve MN scores**
   ```sh
   curl "http://localhost:8016/mntest/result?userId=user123"
   # Expected: {"userId":"user123","traitScores":{...}}
   ```

## 3. Vector Search Service
1. **Glossary query**
   ```sh
   curl -X POST http://localhost:8017/vector/search \
        -H "Content-Type: application/json" \
        -d '{"query":"What does Creative mean?","glossaryType":"mn","top_k":3}'
   # Expect a JSON array of 3 chunks: [{"title":...,"chunk":...,"topic":...},...]
   ```

## 4. Storage Service (Session Memory & Summaries)
Define a session ID for testing (e.g., in your shell):
```bash
export SESSION_ID=test-session-1
```
1. **Fetch empty session**
   ```sh
   curl http://localhost:8011/memory/get/$SESSION_ID
   # Expected: []
   ```
2. **Save a user+assistant pair**
   ```sh
   curl -X POST http://localhost:8011/memory/save \
        -H "Content-Type: application/json" \
        -d '{
            "userId":"user123",
            "sessionId":"'$SESSION_ID'",
            "messages":[
                {"role":"user","content":"Hello"},
                {"role":"assistant","content":"Hi there!"}
            ]
        }'
   # Expected: HTTP 204 No Content
   ```
3. **Fetch saved session**
   ```sh
   curl http://localhost:8011/memory/get/$SESSION_ID
   # Expected: [
   #   {"role":"user","content":"Hello"},
   #   {"role":"assistant","content":"Hi there!"}
   # ]
   ```
4. **Get summary (none yet)**
   ```sh
   curl http://localhost:8011/memory/summary/$SESSION_ID
   # Expected: {}
   ```
5. **Expire session manually**
   ```sh
   curl -X POST http://localhost:8011/memory/expire \
        -H "$AUTH_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"uuid":"'$SESSION_ID'"}'
   # Expected: HTTP 204
   ```
6. **Fetch summary after expire**
   ```sh
   curl http://localhost:8011/memory/summary/$SESSION_ID \
        -H "$AUTH_TOKEN"
   # Expected: {"summary_text":"...","full_transcript":{...},"created_at":"..."}
   ```

## 5. Chat Service
1. **Health check**
   ```sh
   curl http://localhost:8015/health
   # Expected: {"status":"ok","service":"chat"}
   ```
2. **Chat query**
   ```sh
   curl -X POST http://localhost:8015/query \
        -H "$AUTH_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
            "userId":"user123",
            "username":"tester",
            "fullName":"Test User",
            "traitScores": {"creative": 8.4, "logical": 6.1, "administrative": 3.2},
            "message":"Hello, what does my Creative score imply?",
            "sessionId":"'$SESSION_ID'"
        }'
   # Expected: JSON with "answer" (string), "sources" (array), and placeholders "plan", "critique", "followup".
   ```

---
Record any failures and correct the issues before proceeding to staging/deployment.

**Next Steps**
- Add automated pytest/httpx smoke tests.  
- Instrument logging & metrics.  
- Harden security on internal endpoints.  

Good luck and let’s ship this MVP! 🚀