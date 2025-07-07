import math
import time
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import date
from .tables import Language, Unit, Vocabulary, GrammarRule, CalligraphyCharacter, Exercise

def update_score(score: float, last_seen: date, success: bool) -> float:
    days = (date.today() - last_seen).days
    
    # Time-weighted score using log curve to model memory decay, calibrated for a 2x increase in weight per day
    time_weight = math.log(days + 2) * 2
    print(time_weight)

    # Final score: correctness modulated by time since last seen
    score += success * time_weight - (1-success) * time_weight

    return min(max(0, score), 100)

def orm_to_dict(instance: DeclarativeMeta) -> dict:
    """
    Automatically converts any SQLAlchemy ORM instance to a dictionary of its column values.

    Args:
        instance (DeclarativeMeta): An instance of a SQLAlchemy declarative class.

    Returns:
        dict: Dictionary of the instance's column names and their values.
    """
    result = {}
    for column in instance.__table__.columns:
        value = getattr(instance, column.name)
        # Optionally convert date/datetime to string
        if isinstance(value, date):
            value = value.isoformat()
        result[column.name] = value
    return result

def str_to_modelclass(element_id: str) -> DeclarativeMeta:
    """
    Converts a string representation of a model class to the actual SQLAlchemy model class.

    Args:
        model_str (str): The string representation of the model class.

    Returns:
        DeclarativeMeta: The corresponding SQLAlchemy model class, or None if not found.
    """
    if len(element_id.split("_"))==1:
        model_str = "l"
    elif len(element_id.split("_"))==2:
        model_str = "u"
    else:
        model_str = element_id.split("_")[-1].lower()[0]

    alias_map = {
        Language: ["lang", "l"],
        Unit: ["unit", "u"],
        Vocabulary: ["voc", "v"],
        GrammarRule: ["gram", "g"],
        CalligraphyCharacter: ["char", "c"],
        Exercise: ["ex", "e"]
    }
    for model_class, aliases in alias_map.items():
        if model_str.lower() in aliases:
            return model_class
    raise ValueError(f"Unknown element_id: {element_id}")