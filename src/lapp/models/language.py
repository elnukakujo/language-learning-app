from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from ..core.database import Base
from .unit import Unit

class Language(Base):
    __tablename__ = 'language'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    native_name = Column(String)
    level = Column(String)
    description = Column(String, default="")
    score = Column(Integer, default=0)
    last_seen = Column(Date, default=date.today)
    flag = Column(String, default="")

    # Foreign key to current unit
    current_unit = Column(String, ForeignKey("unit.id"), nullable=True)

    # One-to-many: all units belonging to this language
    units: Mapped[list["Unit"]] = relationship(
        "Unit",
        back_populates="parent",
        cascade="all, delete-orphan",
        foreign_keys=lambda: [Unit.language_id]
    )

    # One-to-one: current unit relationship (optional, but useful)
    current_unit_obj: Mapped["Unit"] = relationship(
        "Unit",
        foreign_keys=[current_unit],
        uselist=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "native_name": self.native_name,
            "level": self.level,
            "description": self.description,
            "score": self.score,
            "last_seen": self.last_seen.isoformat(),
            "flag": self.flag,
            "current_unit": self.current_unit
        }