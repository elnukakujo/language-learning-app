from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from ..core.database import Base
from .unit import Unit

class Vocabulary(Base):
    __tablename__ = 'vocabulary'
    
    id = Column(String, primary_key=True, index=True)
    word = Column(String, index=True)
    translation = Column(String)
    phonetic = Column(String, default="")
    example_sentence = Column(String, default="")
    type = Column(String, default="")  # e.g., noun, verb, adjective
    score = Column(Integer, default=0)  # e.g., how much the vocabulary is mastered
    last_seen = Column(Date, default=date.today)  # e.g., when the vocabulary was last seen

    parent: Mapped["Unit"] = relationship("Unit", back_populates="vocs")
    unit_id: Mapped[str] = mapped_column(ForeignKey("unit.id"))  # Fixed: should be str, not int

    def to_dict(self):
        return {
            "id": self.id,
            "word": self.word,
            "translation": self.translation,
            "phonetic": self.phonetic,
            "example_sentence": self.example_sentence,
            "type": self.type,
            "score": self.score,
            "last_seen": self.last_seen.isoformat(),
            "unit_id": self.unit_id
        }