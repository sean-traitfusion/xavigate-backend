# backend/prompt_engine/engine.py
from typing import List, Dict, Optional
import random

# --- Example prompt pools ---
PROMPT_POOLS = {
    "burnout_risk_flag": [
        "What would help you feel even 5% more resourced right now?",
        "Where is your energy leaking — and what could seal that leak, even temporarily?"
    ],
    "creative_trait_suppression": [
        "What’s something expressive or imaginative you’ve been pushing aside?",
        "What would it feel like to play again — just for you?"
    ],
    "mentor_path_ready": [
        "Where might your lived experience help someone else grow?",
        "What’s a gift you carry that’s meant to be passed on?"
    ],
    "default_QI": [
        "What’s expanding in your world right now?",
        "Where are you already in flow — and what supports that?"
    ],
    "default_QII": [
        "Where are you succeeding outwardly but drifting inwardly?",
        "What looks good on the outside but feels off on the inside?"
    ],
    "default_QIII": [
        "What feels heavy, blocked, or out of reach lately?",
        "If you could name the part of you that feels furthest away, what would it say?"
    ],
    "default_QIV": [
        "What’s alive in you but waiting for permission?",
        "What creative spark or truth is trying to emerge, but hasn’t had space yet?"
    ]
}

# --- Example tone modifiers ---
TONE_MODIFIERS = {
    "poetic": lambda p: f"\u2728 {p} (Say it like a whisper to your future self...)",
    "strategic": lambda p: f"What’s one small action you can take here? {p}",
    "gentle": lambda p: f"No pressure. Just explore: {p}",
    "direct": lambda p: f"Cut to the chase: {p}"
}


def select_prompt(
    quadrant: str,
    active_tags: List[str],
    avatar_tone: Optional[str] = None,
    avatar_name: Optional[str] = None,  # ✅ NEW
    default_tone: str = "gentle"
) -> str:
    """
    Chooses a prompt based on alignment quadrant, tags, and avatar tone.
    If avatar_name is provided, adds a voice-style suggestion.
    """
    tag_priority_order = [
        "burnout_risk_flag",
        "creative_trait_suppression",
        "mentor_path_ready",
    ]

    # 1. Use tag-specific prompt if present
    for tag in tag_priority_order:
        if tag in active_tags and tag in PROMPT_POOLS:
            prompt = random.choice(PROMPT_POOLS[tag])
            break
    else:
        # 2. Fallback to quadrant-based default prompt
        prompt = random.choice(PROMPT_POOLS.get(f"default_{quadrant}", ["What’s real right now?"]))

    # 3. Apply tone modifier if applicable
    tone_fn = TONE_MODIFIERS.get(avatar_tone or default_tone)
    if tone_fn:
        prompt = tone_fn(prompt)

    # 4. Inject voice style from avatar_name if present
    if avatar_name:
        prompt = f"[Respond in the style and energy of {avatar_name}]\n\n{prompt}"

    return prompt
