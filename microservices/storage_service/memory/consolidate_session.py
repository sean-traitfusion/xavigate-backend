# /backend/memory/consolidate_session.py
from memory.models import UserMemory
from uuid import UUID
import json

def synthesize_persistent_update(uuid: UUID, plan: dict, critique: str) -> UserMemory:
    """
    Converts session-level insights into persistent memory updates.
    """

    # You can refine this logic later
    traits = []
    if "burnout" in plan.get("emphasize_tags", []):
        traits.append("burnout_risk")

    personality_scores = {
        "clarity": 0.8 if "clarify" in plan.get("target_goal", "") else 0.5
    }

    return UserMemory(
        uuid=uuid,
        initial_personality_scores=personality_scores,
        score_explanations={"clarity": "Detected focus on internal misalignment"},
        trait_history={"tags_from_session": plan.get("emphasize_tags", [])},
        preferences={},
    )