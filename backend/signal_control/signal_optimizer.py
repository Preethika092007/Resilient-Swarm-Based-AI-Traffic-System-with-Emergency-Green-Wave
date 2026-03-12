"""
Module for calculating traffic priorities and green signal timings.
"""
from typing import Dict, List, Tuple
import config

def calculate_priority_score(vehicle_count: int, waiting_time: int, is_emergency: bool = False) -> float:
    """
    Calculates the priority score for a lane.
    If emergency signal is detected, the score is boosted significantly.
    """
    if is_emergency:
        # High score to ensure it ranks first
        return 1000.0 + vehicle_count + waiting_time
    
    return float(vehicle_count + waiting_time)

def calculate_green_time(priority_score: float) -> int:
    """
    Formula: green_time = base_time + priority_score * factor
    Capped by MAX_GREEN_TIME unless it's an emergency.
    """
    # Check if it was an emergency (indicated by score > 1000)
    if priority_score >= 1000:
        return config.EMERGENCY_GREEN_TIME
    
    green_time = config.BASE_TIME + (priority_score * config.PRIORITY_FACTOR)
    return min(int(green_time), config.MAX_GREEN_TIME)

def rank_lanes(traffic_data: Dict[str, Dict]) -> List[Tuple[str, float]]:
    """
    Ranks lanes berdasarkan priority score.
    Returns a sorted list of (lane_id, priority_score).
    """
    lane_scores = []
    for lane_id, data in traffic_data.items():
        score = calculate_priority_score(
            data.get("vehicle_count", 0),
            data.get("waiting_time", 0),
            data.get("emergency", False)
        )
        lane_scores.append((lane_id, score))
    
    # Sort by score descending
    return sorted(lane_scores, key=lambda x: x[1], reverse=True)
