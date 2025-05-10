from typing import Dict
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def critique_assistant_response(plan: Dict, response: str) -> str:
    """
    Uses GPT to critique the assistant's output against the original plan.
    Returns a private reflection, not shown to the user.
    """

    goal = plan.get("target_goal", "unknown goal")
    tone = plan.get("avatar_tone", "neutral")
    emphasized_tags = ", ".join(plan.get("emphasize_tags", [])) or "none"

    system_prompt = f"""
You are a reflective diagnostic evaluator. Your job is to critique an assistant's performance.

You will be given:
- The assistant's intended goal, tone, and emphasized tags (the plan)
- The actual response the assistant gave

Return a short critique (2-4 sentences) evaluating:
- Whether the tone matched the plan
- Whether the response addressed the intended goal
- Whether the emphasized tags showed up in the assistant's language or logic

Be constructive. This will be used to improve future responses. Do not suggest rewriting the response, just critique it.
""".strip()

    user_prompt = f"""
Plan:
- Goal: {goal}
- Tone: {tone}
- Emphasized Tags: {emphasized_tags}

Assistant's Response:
\"\"\"
{response}
\"\"\"
""".strip()

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"⚠️ CritiqueAgent failed: {e}")
        return ""