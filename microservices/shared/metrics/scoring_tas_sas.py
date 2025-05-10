# backend/metrics/scoring_tas_sas.py
from typing import List, Dict

def score_tas(traits_used: List[str], traits_suppressed: List[str]) -> int:
    """
    Returns Trait Alignment Score (0–10)
    High score = many core traits in active use; low = suppressed or distorted.
    """
    usage_count = len(traits_used)
    suppression_count = len(traits_suppressed)

    if usage_count == 0:
        return 2 if suppression_count > 0 else 1
    if usage_count >= 4 and suppression_count == 0:
        return 9
    if usage_count >= 3 and suppression_count <= 1:
        return 7
    if usage_count == 2:
        return 5
    return 3

def score_sas(support_level: str, blockers: List[str]) -> int:
    """
    support_level: 'Yes' | 'Sometimes' | 'No'
    blockers: list of frictional elements (optional)
    Returns Situational Alignment Score (0–10)
    """
    if support_level == "Yes" and not blockers:
        return 9
    if support_level == "Yes" and blockers:
        return 7
    if support_level == "Sometimes":
        return 5 if blockers else 6
    if support_level == "No":
        return 2 if blockers else 3
    return 4  # fallback
