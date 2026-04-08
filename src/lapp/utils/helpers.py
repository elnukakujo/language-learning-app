from datetime import date
from math import log2

def update_score(
    score: float,
    last_seen: date,
    similarity: float,  # 0.0 to 1.0 or 0 to 100
    difficulty: float = 0.5,  # 0.0 (easy) to 1.0 (hard)
    scale: float = 5.0, # The score given for a perfect answer on day one with default difficulty and recency
    recency_bonus: float = 1.0
) -> float:
    remaining_days = (date.today() - last_seen).days

    # Language-specific time decay: slower for hard words, faster for easy ones
    # Adjust log curve based on difficulty

    time_weight = log2(remaining_days + 2) * scale * (1 + difficulty) * recency_bonus

    # Score update: similarity modulates the time weight
    # Partial success (e.g., 0.7) gives partial benefit
    score += similarity * time_weight - (1 - similarity) * time_weight * 0.5  # Penalty for mistakes

    # Ensure score stays within bounds
    return min(max(0, score), 100)