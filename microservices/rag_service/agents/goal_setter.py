from storage_service.session.session_state import SessionState
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def suggest_goal_from_context(prompt: str, session_state: SessionState) -> str:
    """
    Uses GPT to suggest a relevant session goal based on the user's prompt, quadrant, tags, and past context.
    """

    history_snippets = "\n".join([
        f"User: {e.user_prompt}\nAssistant: {e.assistant_response}"
        for e in session_state.history[-3:]  # last 3 for brevity
    ]) or "No prior exchanges."

    tag_list = ", ".join([t.tag_id for t in session_state.recent_tags]) or "None"

    system_prompt = f"""
You are a diagnostic agent assistant. Your job is to help clarify the user's session focus based on their current question, alignment quadrant, recent tags, and conversation history.

Output a one-sentence goal such as:
- "clarify source of burnout"
- "explore internal resistance to creative expression"
- "identify habits causing misalignment"
- "review recent energy drains"

Do not explain. Just output the goal.

Quadrant: {session_state.quadrant}
Tags: {tag_list}

Recent Context:
{history_snippets}
""".strip()

    user_prompt = f"The user just said: {prompt}\n\nWhat is the most useful session goal right now?"

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4
        )
        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"⚠️ GoalSetterAgent failed: {e}")
        return ""