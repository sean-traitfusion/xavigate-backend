#!/usr/bin/env python3
"""
Reset configuration to Xavigate defaults
"""
import httpx
import asyncio
import os
import sys

DEFAULT_SYSTEM_PROMPT = """You are Xavigate, an experienced Multiple Natures (MN) practitioner and personal life guide. You help people understand and align their unique constellation of traits to achieve greater fulfillment and success.

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

Remember: You're not just answering questions - you're helping them understand how their unique trait constellation influences their experiences and guiding them toward greater alignment."""

async def reset_config():
    token = os.getenv("COGNITO_TOKEN")
    if not token:
        print("❌ Please set COGNITO_TOKEN environment variable")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    config = {
        # Essential fix - save BOTH keys
        "system_prompt": DEFAULT_SYSTEM_PROMPT,
        "SYSTEM_PROMPT": DEFAULT_SYSTEM_PROMPT,
        "conversation_history_limit": 5,
        "CONVERSATION_HISTORY_LIMIT": 5,
        "top_k_rag_hits": 5,
        "TOP_K_RAG_HITS": 5,
        "prompt_style": "default",
        "PROMPT_STYLE": "default",
        "model": "gpt-3.5-turbo",
        "MODEL": "gpt-3.5-turbo",
        "temperature": 0.7,
        "TEMPERATURE": 0.7,
        "max_tokens": 1000,
        "MAX_TOKENS": 1000,
        "presence_penalty": 0.1,
        "PRESENCE_PENALTY": 0.1,
        "frequency_penalty": 0.1,
        "FREQUENCY_PENALTY": 0.1,
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:8011/api/memory/runtime-config",
            headers=headers,
            json=config
        )
        
        if resp.status_code == 200:
            print("✅ Configuration reset to Xavigate defaults!")
            print("\nYou can now:")
            print("1. Visit http://localhost:8012/dashboard/")
            print("2. Modify the system prompt")
            print("3. Save your changes")
            print("4. Test your changes")
        else:
            print(f"❌ Failed: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    asyncio.run(reset_config())