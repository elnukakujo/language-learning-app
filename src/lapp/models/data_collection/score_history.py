from sqlalchemy import Column, Float, String

from ...core. database import db_manager
from ..base import BaseDataCollectionModel
from ...utils import resolve_element_model

class ScoreHistory(BaseDataCollectionModel):
    __tablename__ = 'score_history'

    element_type = Column(String, nullable=False)
    score_before = Column(Float, nullable=False)
    score_after = Column(Float, nullable=False)

    # Foreign keys
    element_id = Column(String, nullable=False)  # No FK — BaseElementModel is abstract

    def get_element(self):
        """Resolve element_id to its concrete model instance."""
        if not self.element_id:
            return None
        
        model_class = resolve_element_model(self.element_id)
        if model_class is None:
            raise ValueError(f"Unknown element prefix in id '{self.element_id}'")
        
        return db_manager.find_by_attr(model_class, {id: self.element_id})

    def to_dict(self, include_relations: bool = True) -> dict:
        base = {
            **super().to_dict(),
            "element_id": self.element_id,
            "element_type": self.element_type,
            "score_before": self.score_before,
            "score_after": self.score_after,
        }
        if include_relations:
            base["element"] = self.get_element().to_dict() if self.get_element() else None
        return base