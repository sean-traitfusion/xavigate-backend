Xavigate Backend Integration Guide
================================

Overview
--------
The Xavigate Backend provides a set of FastAPI microservices to support authentication, personality testing,
vector-based glossary lookups, session memory storage, and chat orchestration.  Each service runs in its
own container and is exposed via an NGINX API gateway on port 8080.

Prerequisites & Environment
---------------------------
1. Ensure you have Docker and Docker Compose installed.
2. In the project root, create or update the `.env` file with at least the following:
   ENV=dev
   POSTGRES_DB=xavigate
   POSTGRES_USER=xavigate_user
   POSTGRES_PASSWORD=changeme
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   DATABASE_URL=postgresql://xavigate_user:changeme@postgres:5432/xavigate
   OPENAI_API_KEY=<your-openai-key>      # for Vector/RAG embeddings in prod
   XAVIGATE_KEY=supersecuredevkey       # shared API key for auth in dev

   Note: per-service `.env` files are git-ignored; the root `.env` is authoritative.

3. Start all services:
   docker-compose up --build -d

API Gateway (NGINX)
------------------
Base URL: http://localhost:8080/api

Routes:
  /api/auth/    -> Auth Service (port 8014)
  /api/rag/     -> RAG Service (port 8010)
  /api/vector/  -> Vector Search Service (port 8017)
  /api/storage/ -> Storage Service (port 8011)
  /api/chat/    -> Chat Service (port 8015)
  /api/mntest/  -> MNTest Service (port 8016)
  /api/stats/   -> Stats Service (port 8012)
  /api/db/      -> DB Service (port 8013)

Authentication
--------------
- In dev mode (ENV=dev), authentication is disabled: no headers required.
- In prod mode (ENV=prod), every request (except health) requires:
    Header: X-XAVIGATE-KEY: <value from .env>

Service Endpoints
-----------------

1. Auth Service
   GET  /auth/health
     Response: {"status":"ok","service":"auth"}

   POST /auth/verify
     Headers: Content-Type: application/json
     Body: {"key":"<token-or-api-key>"}
     Response: {"valid":true,"sub":null}

2. MNTest Service
   GET  /mntest/health
     Response: {"status":"ok","service":"mntest"}

   POST /mntest/submit
     Headers: Content-Type: application/json
     Body: {
       "userId":"user123",
       "traitScores": {"creative":8.4, "logical":6.1, "administrative":3.2}
     }
     Response: {"status":"ok"}

   GET  /mntest/result?userId=user123
     Response: {"userId":"user123","traitScores":{...}}

3. Vector Search Service
   POST /vector/search
     Headers: Content-Type: application/json
     Body: {"query":"What does Creative mean?","glossaryType":"mn","top_k":3}
     Response: [
       {"title":"Creative","chunk":"Creative is ...","topic":"Trait","score":1.0},
       ...
     ]

4. Storage Service (Session Memory & Summaries)
   GET  /storage/session-memory/{sessionId}
     Response (dev): {"exchanges":[{"role":"user","content":"Hello"},...]}

   POST /storage/session-memory
     Headers: Content-Type: application/json
     Body: {"uuid":"sessionId","conversation_log":{"exchanges":[...]}}
     Response: {"status":"session memory updated"}

   GET  /storage/get/{sessionId}
     Response: [{"role":"user","content":"Hello"},...]

   POST /storage/save
     Headers: Content-Type: application/json
     Body: {
       "userId":"user123",
       "sessionId":"sessionId",
       "messages":[{"role":"user","content":"Hello"},...]
     }
     Response: HTTP 204 No Content

   GET  /storage/summary/{sessionId}
     Response (dev): {}

   POST /storage/expire
     Headers: Content-Type: application/json
     Body: {"uuid":"sessionId"}
     Response: HTTP 204

5. Chat Service
   POST /chat/query
     Headers:
       Content-Type: application/json
       Authorization: Bearer <token>   # omit in dev
     Body: {
       "userId":"user123",
       "username":"tester",
       "fullName":"Test User",
       "traitScores":{...},
       "message":"Hello, what does my Creative score imply?",
       "sessionId":"sessionId"
     }
     Response:
       {
         "answer":"<string>",
         "sources":[{"text":"...","metadata":{...}},...],
         "plan":{},
         "critique":"",
         "followup":""
       }

6. RAG Service
   GET  /rag/health
     Response: {"status":"ok","service":"rag"}
   POST /rag/query
     (See RAG service docs for full schema.)

Notes
-----
- All endpoints are prefixed with `/api` when using the NGINX gateway.
- In production, remove any dev-mode stubs and ensure `ENV=prod` is set in the root `.env`.
- Consult individual service READMEs for advanced configuration.