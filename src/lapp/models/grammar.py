from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from ..core.database import Base
from .unit import Unit

class Grammar(Base):
    __tablename__ = 'grammar'
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    explanation = Column(String)
    learnable_sentence = Column(String, default="")
    score = Column(Integer, default=0)
    last_seen = Column(Date, default=date.today)  # e.g., when the grammar rule was last seen

    parent: Mapped["Unit"] = relationship("Unit", back_populates="grammars")
    unit_id: Mapped[str] = mapped_column(ForeignKey("unit.id"))  # Fixed: should be str, not int

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "explanation": self.explanation,
            "learnable_sentence": self.learnable_sentence,
            "score": self.score,
            "last_seen": self.last_seen.isoformat(),
            "unit_id": self.unit_id
        }