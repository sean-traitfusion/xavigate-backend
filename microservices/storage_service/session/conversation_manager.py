from typing import Dict
from .session_state import SessionState

def route(session_state: SessionState) -> Dict:
    profile = session_state.avatar_profile

    plan = {
        "next_action": "respond_with_rag",
        "avatar_name": profile.avatar_id if profile else "wise_mentor",
        "avatar_tone": profile.prompt_framing if profile and profile.prompt_framing else "supportive coach",
        "target_goal": session_state.goal or "continue guided reflection",
        "emphasize_tags": [],
        "comment_on": None,
        "handoff_to_agent": None,
    }

    if session_state.quadrant == "Overdrive":
        plan["target_goal"] = "prompt rest and boundary-setting"
        plan["comment_on"] = "You're showing signs of Overdrive — are you taking time to recharge?"

    if any("burnout" in t.tag_id.lower() for t in session_state.recent_tags):
        plan["emphasize_tags"].append("burnout")

    if session_state.quadrant == "Drift":
        plan["handoff_to_agent"] = "GoalSettingAgent"

    return plan