from datetime import date
from math import log2


def compute_recency_weight(
    created_at: date,
    last_seen: date
) -> float:
    """
    Computes a recency weight from both created_at and last_seen.

    - staleness:  how long since last review  → increases weight (more forgetting)
    - maturity:   how long since item created → decreases weight (well-learned items need less boost)
    """
    today = date.today()

    days_since_seen    = (today - last_seen).days
    days_since_created = (today - created_at).days

    staleness       = log2(days_since_seen + 2)
    maturity_dampen = log2(days_since_created + 2)

    return staleness / maturity_dampen

def update_score(
    score: float,
    last_seen: date,
    similarity: float,        # 0.0 to 1.0
    created_at: date = date.today(),
    difficulty: float = 0.5,  # 0.0 (easy) to 1.0 (hard)
    scale: float = 5.0
) -> float:
    """
    Updates the score for any Feature or Component after a review session.

    Args:
        score:        Current score (0–100)
        created_at:   Date the item was first created/added
        last_seen:    Date the item was last reviewed
        similarity:   Answer quality (0.0 = wrong, 1.0 = perfect)
        difficulty:   Current difficulty ratio (0.0 = easy, 1.0 = hard)
        scale:        Score given for a perfect answer on day one
    """
    remaining_days  = (date.today() - last_seen).days
    recency_weight  = compute_recency_weight(created_at, last_seen)

    # Slower decay for hard items, faster for easy ones, modulated by recency
    time_weight = log2(remaining_days + 2) * scale * (1 + difficulty) * recency_weight

    # Partial success gives partial benefit; mistakes apply a half-weight penalty
    score += similarity * time_weight - (1 - similarity) * time_weight * 0.5

    return round(min(max(0.0, score), 100.0), 4)


def update_difficulty(
    new_score: float,
    last_seen: date,
    previous_difficulty: float,  # Initialize as 0.5 if no prior value
    created_at: date = date.today(),
    scale: float = 1.0,
    alpha: float = 0.3           # EMA learning rate: higher = more reactive
) -> float:
    """
    Updates the difficulty ratio for any Feature or Component based on score performance.

    Args:
        new_score:           Score after calling update_score() (0–100)
        created_at:          Date the item was first created/added
        last_seen:           Date the item was last reviewed
        previous_difficulty: Prior difficulty (0.0 = easy, 1.0 = hard)
        scale:               Sensitivity of difficulty shift
        alpha:               EMA learning rate (0.0 = ignore new signal, 1.0 = fully reactive)
    """
    recency_weight = compute_recency_weight(created_at, last_seen)

    # Normalize score to 0–1 performance signal
    performance = new_score / 100.0

    # Poor performance → push difficulty UP; strong performance → pull it DOWN
    # Centered at 0.5 performance as the neutral point
    difficulty_delta = (0.5 - performance) * scale * recency_weight * 0.1

    # Exponential moving average for stability across sessions
    new_difficulty = (1 - alpha) * previous_difficulty + alpha * (previous_difficulty + difficulty_delta)

    return min(max(0.0, new_difficulty), 1.0)