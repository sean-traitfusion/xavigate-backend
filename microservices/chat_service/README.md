# Chat Service

This FastAPI service exposes a single `/chat` endpoint for turn-level orchestration of user prompts.  It is backed by stubbed calls to downstream microservices (Auth, RAG, Storage, Stats) when running in development mode.

## Quickstart (Development)

1. Ensure Docker & Docker Compose are installed.
2. From the repo root, build and start the service along with its dependencies:
   ```bash
   docker compose up --build chat_service auth_service rag_service storage_service stats_service db_service nginx
   ```
3. The chat-service will be available at `http://localhost:8015` (health-check) and proxied via NGINX at `http://localhost:8080/api/chat`.

## API Documentation

- Swagger UI:  `GET http://localhost:8080/api/chat/docs`
- Redoc:       `GET http://localhost:8080/api/chat/redoc`
- OpenAPI JSON: `GET http://localhost:8080/api/chat/openapi.json`

### POST /chat

Request Body (application/json):
```json
{
  "prompt": "string",       // the user query
  "user_id": "string|null",// optional user identifier
  "top_k": 3,               // optional number of RAG hits
  "tags": "string|null"    // optional comma-separated filter tags
}
```

Response Body (application/json):
```json
{
  "answer": "string",      // the assistant's response (stub or real)
  "sources": [              // array of RAG Document objects
    { "text": "string", "metadata": {} }
  ],
  "plan": {},               // orchestration plan data
  "critique": "string",    // CritiqueAgent output
  "followup": "string"     // FollowUpAgent suggestion
}
```

## Environment Variables (`.env`)
```ini
ENV=dev
AUTH_URL=http://auth_service:8014
RAG_URL=http://rag_service:8010
STORAGE_URL=http://storage_service:8011
STATS_URL=http://stats_service:8012
XAVIGATE_KEY=changeme
OPENAI_API_KEY=           # fill in for real LLM calls
```

## Testing

Run the contract smoke tests:
```bash
cd microservices/chat_service
pytest -q
```

## Frontend Integration

1. Use the Swagger UI or OpenAPI JSON as your contract.
2. (Optional) Generate a TypeScript client with:
   ```bash
   npx openapi-typescript-codegen --input ./openapi.json --output ../frontend/src/api/chat --client axios
   ```
3. Begin wiring your UI calls to `POST /api/chat/chat` via `http://localhost:8080` gateway.

Once the frontend team confirms the API shape, we will replace the stubs in `client.py` with real HTTP calls, integrate OpenAI, and implement persistent session logging and analytics.