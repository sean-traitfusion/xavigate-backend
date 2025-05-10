# backend/tags/infer_tags.py
from typing import List, Dict
from storage_service.memory.models import AlignmentTag
from datetime import datetime

def infer_alignment_tags(
    reflection: str,
    ax_history: List[float],
    traits_used: List[str],
    traits_suppressed: List[str],
) -> List[AlignmentTag]:
    tags: List[AlignmentTag] = []
    now = datetime.now()

    reflection = reflection.lower()

    # 🔥 Burnout risk tag
    if any(w in reflection for w in ["tired", "burnt", "drained", "exhausted", "flat"]):
        tags.append(AlignmentTag(
            tag_id="burnout_risk_flag",
            category="emotional_risk",
            trigger_source="reflection",
            priority_level=9,
            memory_scope="session",
            first_triggered_at=now,
        ))

    # 🎭 Creative trait suppression
    if "Creative" in traits_suppressed:
        tags.append(AlignmentTag(
            tag_id="creative_trait_suppression",
            category="trait_misalignment",
            trigger_source="trait_check",
            priority_level=5,
            memory_scope="session",
            first_triggered_at=now,
        ))

    # 🌪️ Alignment volatility
    if len(ax_history) >= 4:
        recent_deltas = [abs(ax_history[i+1] - ax_history[i]) for i in range(-4, -1)]
        if max(recent_deltas) > 25:
            tags.append(AlignmentTag(
                tag_id="alignment_volatility_flag",
                category="quadrant_pattern",
                trigger_source="ax_history",
                priority_level=7,
                memory_scope="persistent",
                first_triggered_at=now,
        ))

    # 🌱 Mentor readiness (high recent AX average + Creative or Strategic traits used)
    if len(ax_history) >= 3:
        recent_avg = sum(ax_history[-3:]) / 3
        if recent_avg > 80 and any(t in traits_used for t in ["Creative", "Strategic", "Providing"]):
            tags.append(AlignmentTag(
                tag_id="mentor_path_ready",
                category="growth_signal",
                trigger_source="pattern_recognition",
                priority_level=8,
                memory_scope="persistent",
                first_triggered_at=now,
            ))

    return tags
