from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from ..core.database import Base
from .unit import Unit

class Character(Base):
    __tablename__ = 'character'

    id = Column(String, primary_key=True, index=True)
    character = Column(String, index=True)  # e.g., the character itself
    components = Column(String, default="")
    phonetic = Column(String)  # e.g., pinyin for Chinese characters
    meaning = Column(String)
    example_word = Column(String, default="")
    score = Column(Integer, default=0)  # e.g., how much the character is mastered
    last_seen = Column(Date, default=date.today)  # e.g., when the character was last seen

    parent: Mapped["Unit"] = relationship("Unit", back_populates="characters")
    unit_id: Mapped[str] = mapped_column(ForeignKey("unit.id"))  # Fixed: should be str, not int

    def to_dict(self):
        return {
            "id": self.id,
            "character": self.character,
            "components": self.components,
            "phonetic": self.phonetic,
            "meaning": self.meaning,
            "example_word": self.example_word,
            "score": self.score,
            "last_seen": self.last_seen.isoformat(),
            "unit_id": self.unit_id
        }