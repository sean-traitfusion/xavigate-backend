# backend/metrics/scoring_aq.py
from typing import Dict

# 7 AQ dimensions expected as keys with 0–10 integer values
def score_aq(dimensions: Dict[str, int]) -> float:
    """
    Normalize raw AQ input to a 0-100 scale.
    """
    total = sum(dimensions.values())
    return round((total / 70) * 100, 1)

# Optional tier classification (can be used for tone logic)
def classify_aq(score: float) -> str:
    if score <= 30:
        return "Emerging"
    if score <= 55:
        return "Developing"
    if score <= 75:
        return "Skilled"
    if score <= 90:
        return "Advanced"
    return "Mastering"

# Sample AQ dimensions expected:
# {
#   "reflection_depth": 6,
#   "action_responsiveness": 7,
#   "recalibration_speed": 5,
#   "alignment_literacy": 6,
#   "self_initiated_behavior": 4,
#   "feedback_integration": 6,
#   "emotional_regulation": 7
# }
