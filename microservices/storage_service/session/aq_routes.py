# backend/session/aq_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from shared.metrics.scoring_aq import score_aq, classify_aq
from memory.storage import load_user_profile, save_user_profile
from datetime import datetime

router = APIRouter()

class AQInput(BaseModel):
    user_id: str
    reflection_depth: int
    action_responsiveness: int
    recalibration_speed: int
    alignment_literacy: int
    self_initiated_behavior: int
    feedback_integration: int
    emotional_regulation: int

@router.post("/api/session/aq")
async def aq_handler(payload: AQInput):
    dimensions = payload.dict()
    user_id = dimensions.pop("user_id")

    aq = score_aq(dimensions)
    tier = classify_aq(aq)

    profile = load_user_profile(user_id)
    if not profile:
        raise ValueError("User not found")

    profile.baseline_aq = aq
    profile.alignment_quotient_history.append(aq)
    save_user_profile(profile)

    return {
        "aq": aq,
        "tier": tier,
        "message": f"AQ score is {aq} — classified as {tier}."
    }
