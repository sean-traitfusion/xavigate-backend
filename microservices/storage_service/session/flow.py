# backend/session/flow.py
from datetime import datetime
from typing import Optional, Dict, Any
import random

from storage_service.memory.storage import load_user_profile, save_user_profile, save_session_record
from storage_service.memory.models import SessionRecord
from shared.metrics.scoring_tas_sas import score_tas, score_sas
from shared.metrics.scoring_ass import score_ass
from shared.tags.infer_tags import infer_alignment_tags
from shared.tags.promote_tags import promote_session_tags

# Placeholder prompt library (to be replaced with prompt engine later)
PROMPT_LIBRARY = {
    "QI": ["What feels most alive for you right now?", "Where are you being called to stretch?"],
    "QII": ["What's working — but not quite feeding you?", "Where is success feeling a little off?"],
    "QIII": ["What's draining you lately?", "What's feeling stuck, heavy, or missing?"],
    "QIV": ["What part of you wants to emerge — but hasn't had space yet?", "What feels blocked, even if you're showing up?"]
}

def generate_prompt(quadrant: str, tags: list[str]) -> str:
    if "burnout_risk_flag" in tags:
        return "What would feel most replenishing right now — even if it's small?"
    if "creative_trait_suppression" in tags:
        return "What's something creative you wish you had more space to do?"
    return random.choice(PROMPT_LIBRARY.get(quadrant, ["How are you doing really?"]))

def handle_reflection(
    user_id: str,
    reflection_text: str,
    current_quadrant: Optional[str] = None
) -> Dict[str, Any]:
    profile = load_user_profile(user_id)
    if not profile:
        raise ValueError("User not found")

    reflection = reflection_text.lower()
    ax_delta = 0
    if any(w in reflection for w in ["stuck", "tired", "numb", "exhausted"]):
        ax_delta = -10
    elif any(w in reflection for w in ["excited", "energized", "hopeful", "alive"]):
        ax_delta = 10

    new_ax = max(0, min(100, (profile.baseline_ax or 50) + ax_delta))
    profile.alignment_index_history.append(new_ax)

    if new_ax >= 76:
        quadrant = "QI"
    elif new_ax >= 51:
        quadrant = "QII"
    elif new_ax >= 45:
        quadrant = "QIV"
    else:
        quadrant = "QIII"

    profile.quadrant_history.append(quadrant)
    profile.baseline_ax = new_ax

    # 🔍 Recalculate ASS and update
    ass = score_ass(profile.alignment_index_history)
    profile.ass = ass

    # 🏷 Infer tags from reflection + traits + history
    session_tags = infer_alignment_tags(
        reflection=reflection_text,
        ax_history=profile.alignment_index_history,
        traits_used=profile.dominant_traits,
        traits_suppressed=profile.suppressed_traits,
    )

    # Promote tags to persistent memory if needed
    profile.alignment_tags = promote_session_tags(session_tags, profile.alignment_tags)

    save_user_profile(profile)

    record = SessionRecord(
        session_id=str(datetime.now().timestamp()),
        user_id=user_id,
        session_date=datetime.now(),
        ax=new_ax,
        ass=ass,
        quadrant=quadrant,
        summary=f"User reflected: '{reflection_text[:50]}...",
        session_tags=session_tags
    )
    save_session_record(record)

    prompt = generate_prompt(quadrant, [t.tag_id for t in session_tags])

    return {
        "new_ax": new_ax,
        "new_quadrant": quadrant,
        "new_ass": ass,
        "next_prompt": prompt,
        "summary": record.summary,
        "session_tags": [t.tag_id for t in session_tags]
    }
