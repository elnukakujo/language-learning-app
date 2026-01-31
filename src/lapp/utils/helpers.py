from datetime import date
import math

def update_score(score: float, last_seen: date, success: bool) -> float:
    days = (date.today() - last_seen).days
    
    # Time-weighted score using log curve to model memory decay, calibrated for a 2x increase in weight per day
    time_weight = math.log(days + 2) * 10

    # Final score: correctness modulated by time since last seen
    score += success * time_weight - (1-success) * time_weight

    return min(max(0, score), 100)