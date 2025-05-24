<!---
This document guides the frontend team on how to call the MN Test Service and Chat Service APIs.
-->
# Frontend API Reference

## Base URL
- Local Development: `http://localhost:8080/api`
- Production: use domain http://chat.xavigate.com:8080, ensure requests are prefixed with `/api`.

## Authentication
- All protected endpoints accept an `Authorization` header: `Bearer <JWT_TOKEN>`.
- In **development** mode, the header is optional; in **production**, it is required.

---

## MN Test Service
Service to store and retrieve Multiple Natures (MNTEST) trait scores.

### Submit MN Test Scores
- **Endpoint:** `POST /mntest/submit`
- **Description:** Save or update a user's trait scores.
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <JWT_TOKEN>` (prod only)
- **Request Body:**
  ```json
  {
    "userId": "<USER_ID>",
    "traitScores": {
      "nature_one": 7.5,
      "nature_two": 4.0,
      // ... up to 19 traits
    }
  }
  ```
- **Response (200):**
  ```json
  { "status": "ok" }
  ```

#### Example (JavaScript)
```js
async function submitMNScores({ userId, traitScores, token }) {
  const res = await fetch(`${BASE_URL}/mntest/submit`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
    },
    body: JSON.stringify({ userId, traitScores }),
  });
  if (!res.ok) throw new Error(`Submit failed: ${res.status}`);
  return await res.json();
}
```  

### Retrieve MN Test Scores
- **Endpoint:** `GET /mntest/result?userId=<USER_ID>`
- **Description:** Fetch a previously submitted MN test result.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>` (prod only)
- **Response (200):**
  ```json
  {
    "userId": "<USER_ID>",
    "traitScores": { /* same shape as submit */ }
  }
  ```

#### Example (JavaScript)
```js
async function fetchMNScores({ userId, token }) {
  const url = new URL(`${BASE_URL}/mntest/result`);
  url.searchParams.set('userId', userId);
  const res = await fetch(url, {
    headers: {
      ...(token && { 'Authorization': `Bearer ${token}` }),
    },
  });
  if (!res.ok) throw new Error(`Fetch failed: ${res.status}`);
  const data = await res.json();
  // Optionally store locally:
  localStorage.setItem('mntestScores', JSON.stringify(data.traitScores));
  return data.traitScores;
}
```

---

## Chat Service
Service to send user messages (with MN test context) and receive AI-driven responses.

### Send Chat Message
- **Endpoint:** `POST /chat/query`
- **Description:** Submit a chat message along with user context and MNTEST scores; receives AI answer and sources.
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <JWT_TOKEN>` (prod only)
- **Request Body:**
  ```json
  {
    "userId": "<USER_ID>",
    "username": "<USER_NAME>",
    "fullName": "<User Full Name>",
    "traitScores": { /* from MN Test */ },
    "message": "Hello, how can I improve my focus?",
    "sessionId": "<SESSION_ID>"
  }
  ```
- **Response (200):**
  ```json
  {
    "answer": "<AI_RESPONSE>",
    "sources": [
      { "text": "...", "metadata": { "title": "...", "topic": "...", "score": 0.95 } }
      // ...
    ],
    "plan": { /* optional next-step plan */ },
    "critique": "<AI_CRITIQUE>",
    "followup": "<AI_FOLLOW_UP_QUESTION>"
  }
  ```

#### Example (JavaScript)
```js
import { v4 as uuidv4 } from 'uuid';

async function sendMessage({ userId, username, fullName, traitScores, message, token }) {
  // Generate or reuse a sessionId per conversation
  const sessionId = uuidv4();
  const payload = { userId, username, fullName, traitScores, message, sessionId };
  const res = await fetch(`${BASE_URL}/chat/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Chat failed: ${res.status}`);
  return await res.json();
}
```

#### Using the Response
- `answer`: display as assistant reply.
- `sources`: list of context excerpts for reference.
- `plan`, `critique`, `followup`: optional structured elements for UI enhancements.

---

### Constants
```js
const BASE_URL = 'http://localhost:8080/api';
```

---

_End of Frontend API Reference._