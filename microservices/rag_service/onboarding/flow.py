# backend/onboarding/flow.py
from datetime import datetime
from typing import List, Dict, Optional
import json
from pathlib import Path

from shared.metrics.scoring_tas_sas import score_tas, score_sas
from storage_service.memory.models import UserProfile
from storage_service.memory.storage import save_user_profile


def load_trait_bundles(path: str = "onboarding/trait_bundles.json") -> list:
    with open(Path(__file__).parent / path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def run_onboarding(
    user_id: str,
    name: Optional[str],
    traits_used: List[str],
    traits_suppressed: List[str],
    environment_support: str,  # 'Yes', 'Sometimes', 'No'
    environment_blockers: List[str],
    alignment_stage: str = "Early Discovery"
) -> UserProfile:
    """
    Main onboarding handler — scores TAS/SAS, estimates AX, and creates profile
    """
    tas = score_tas(traits_used, traits_suppressed)
    sas = score_sas(environment_support, environment_blockers)
    ax = round((tas + sas) / 2 * 10, 1)  # normalize to 0–100

    profile = UserProfile(
        user_id=user_id,
        name=name,
        onboarding_date=datetime.now(),
        baseline_ax=ax,
        baseline_aq=None,  # Set via future AQ module
        baseline_quadrant=_determine_quadrant(tas, sas),
        alignment_stage=alignment_stage,
        dominant_traits=traits_used,
        suppressed_traits=traits_suppressed,
        alignment_index_history=[ax],
        quadrant_history=[],
        trust_established_flag=True
    )

    save_user_profile(profile)
    return profile


def _determine_quadrant(tas: int, sas: int) -> str:
    """
    Returns quadrant label based on TAS/SAS balance
    """
    if tas >= 7 and sas >= 7:
        return "QI"
    if tas <= 4 and sas <= 4:
        return "QIII"
    if tas >= 6 and sas <= 4:
        return "QIV"
    return "QII"
