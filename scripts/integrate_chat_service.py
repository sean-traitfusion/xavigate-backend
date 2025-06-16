#!/usr/bin/env python3
"""
Script to show how to integrate the enhanced memory system with the chat service
This demonstrates the changes needed in chat_service/main.py
"""

# Example integration code for chat_service/main.py

async def chat_endpoint_enhanced(
    req: ChatRequest,
    authorization: str | None = Header(None, alias="Authorization"),
    _=Depends(require_jwt),
):
    """Enhanced chat endpoint with optimized memory handling"""
    
    if os.getenv("ENV", "dev") == "dev":
        return ChatResponse(answer="Dev stub response", sources=[], plan={}, critique="", followup="")
    
    token = authorization.split(" ", 1)[1] if authorization else ""
    internal_headers = {"Authorization": authorization} if authorization else {}

    async with httpx.AsyncClient() as client:
        # 1. Get persistent memory (user summary)
        persistent_resp = await client.get(
            f"{STORAGE_URL}/api/memory/persistent-memory/{req.userId}",
            headers=internal_headers
        )
        persistent_memory = ""
        if persistent_resp.status_code == 200:
            data = persistent_resp.json()
            persistent_memory = data.get("summary", "")
        
        # 2. Get session memory in new format
        session_resp = await client.get(
            f"{STORAGE_URL}/api/memory/get/{req.sessionId}",
            headers=internal_headers
        )
        session_messages = []
        if session_resp.status_code == 200:
            session_messages = session_resp.json()
        
        # 3. Get runtime config
        try:
            config_resp = await client.get(
                f"{STORAGE_URL}/api/memory/runtime-config",
                headers=internal_headers
            )
            config = config_resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch runtime config: {e}")
        
        # Use config values with overrides
        top_k = req.topK_RAG_hits or config.get("top_k_rag_hits", 5)
        system_prompt = req.systemPrompt or config.get("system_prompt", DEFAULT_PROMPT)
        
        # 4. Get RAG context
        vs_resp = await client.post(
            f"{RAG_URL}/search", 
            json={"query": req.message, "top_k": top_k}
        )
        if vs_resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch glossary chunks")
        chunks = vs_resp.json()
        rag_context = "\n\n".join([c.get("chunk", "") for c in chunks])
        
        # 5. Build user profile section
        profile_parts = [
            f"Name: {req.fullName or 'Unknown'}",
            f"Username: {req.username}",
            "Trait Scores:"
        ]
        for trait, score in req.traitScores.items():
            profile_parts.append(f"- {trait.title()}: {score}")
        
        # Include persistent memory in base prompt if exists
        base_prompt_parts = [system_prompt]
        if req.fullName or req.username:
            base_prompt_parts.append(f"\nUser Profile:\n" + "\n".join(profile_parts))
        
        base_prompt = "\n".join(base_prompt_parts)
        
        # 6. Optimize prompt using the prompt manager
        optimize_resp = await client.post(
            f"{STORAGE_URL}/api/memory/optimize-prompt",
            json={
                "base_prompt": base_prompt,
                "uuid": req.userId,
                "rag_context": rag_context
            },
            headers=internal_headers
        )
        
        if optimize_resp.status_code == 200:
            optimize_data = optimize_resp.json()
            final_prompt = optimize_data["final_prompt"]
            metrics = optimize_data["metrics"]
            
            # Log metrics for monitoring
            print(f"📊 Prompt metrics for {req.userId}:")
            print(f"   Total: {metrics['total_chars']} chars")
            print(f"   Utilization: {metrics['utilization_percent']:.1f}%")
        else:
            # Fallback to manual prompt building
            final_prompt = f"{base_prompt}\n\nCurrent Question: {req.message}"
        
        # 7. Call OpenAI with optimized prompt
        try:
            completion = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": final_prompt}
                ],
                temperature=0.3,
            )
            answer = completion.choices[0].message.content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")
        
        # 8. Save the interaction using new memory endpoint
        save_payload = {
            "userId": req.userId,
            "sessionId": req.sessionId,
            "messages": [
                {"role": "user", "content": req.message},
                {"role": "assistant", "content": answer}
            ]
        }
        
        await client.post(
            f"{STORAGE_URL}/api/memory/save",
            json=save_payload,
            headers=internal_headers
        )
        
        # 9. Build response
        sources = []
        for c in chunks:
            sources.append({
                "text": c.get("chunk", ""),
                "metadata": {
                    "title": c.get("title"),
                    "topic": c.get("topic"),
                    "score": c.get("score"),
                }
            })
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            plan={},
            critique="",
            followup="",
        )


# Additional endpoint to check memory status
@app.get("/memory-status/{userId}")
async def get_memory_status(
    userId: str,
    authorization: str | None = Header(None, alias="Authorization"),
    _=Depends(require_jwt),
):
    """Get memory usage statistics for a user"""
    internal_headers = {"Authorization": authorization} if authorization else {}
    
    async with httpx.AsyncClient() as client:
        stats_resp = await client.get(
            f"{STORAGE_URL}/api/memory/memory-stats/{userId}",
            headers=internal_headers
        )
        
        if stats_resp.status_code == 200:
            return stats_resp.json()
        else:
            raise HTTPException(status_code=stats_resp.status_code, detail="Failed to get memory stats")


# Integration notes:
print("""
📝 INTEGRATION NOTES FOR CHAT SERVICE:

1. Replace the existing chat_endpoint with chat_endpoint_enhanced
2. The new endpoint:
   - Uses persistent memory (user summaries) for better context
   - Optimizes prompt size automatically
   - Uses the new memory save endpoint with voice command detection
   - Provides better memory usage tracking

3. Key improvements:
   - Auto-summarization when session memory fills up
   - Auto-compression of persistent memory
   - Voice command detection ("remember this", etc.)
   - Prompt optimization to stay within token limits

4. To enable in chat_service/main.py:
   - Import the memory optimization endpoint
   - Replace the /query endpoint implementation
   - Add the /memory-status endpoint for monitoring

5. Environment variables needed:
   - SESSION_MEMORY_CHAR_LIMIT (default: 15000)
   - PERSISTENT_MEMORY_CHAR_LIMIT (default: 8000)
   - AUTO_SUMMARY_ENABLED (default: true)
   - AUTO_COMPRESSION_ENABLED (default: true)
""")