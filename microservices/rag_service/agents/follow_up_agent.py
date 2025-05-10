from storage_service.session.session_state import SessionState
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def suggest_follow_up(user_input: str, assistant_response: str, session_state: SessionState) -> str:
    """
    Suggests a follow-up question or prompt to continue the conversation,
    based on what was just said and the user's session context.
    """

    tag_list = ", ".join([t.tag_id for t in session_state.recent_tags]) or "none"
    goal = session_state.goal or "not defined"

    system_prompt = f"""
You are a conversational continuity agent. Based on the user's recent input and the assistant's reply,
suggest a short follow-up question that gently moves the conversation forward.

The follow-up should:
- Align with the session goal
- Be emotionally attuned to the assistant's tone
- Invite reflection or specificity
- Be 1-2 sentences max

Do not restate what was already said. Do not break character.
Just suggest the assistant's next message.
""".strip()

    user_prompt = f"""
Session Goal: {goal}
Tags: {tag_list}

User Input:
\"\"\"
{user_input}
\"\"\"

Assistant's Response:
\"\"\"
{assistant_response}
\"\"\"

What's a good follow-up?
""".strip()

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"⚠️ FollowUpAgent failed: {e}")
        return ""