# backend/metrics/scoring_ass.py
from typing import List
import statistics

def score_ass(ax_history: List[float]) -> float:
    """
    ASS (Alignment Stability Score): based on volatility in AX scores.
    High variance → low stability → lower ASS.
    Low variance → high consistency → higher ASS.
    
    We use a simple formula:
      - Start from 100
      - Subtract scaled standard deviation of AX history
    """
    if len(ax_history) < 3:
        return 50.0  # not enough data yet

    try:
        std_dev = statistics.stdev(ax_history[-5:])  # look at last 5 AX scores
        instability_penalty = min(std_dev * 2, 50)  # cap penalty
        return round(100 - instability_penalty, 1)
    except statistics.StatisticsError:
        return 50.0
