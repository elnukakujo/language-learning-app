from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped

from ..base import BaseContainerModel
from .unit import Unit

class Language(BaseContainerModel):
    __tablename__ = 'language'

    name = Column(String, index=True)
    native_name = Column(String)
    level = Column(String)
    description = Column(String, default="")
    flag = Column(String, default="")

    # Foreign key to current unit
    current_unit = Column(String, nullable=True)

    # One-to-many: all units belonging to this language
    unit: Mapped[list["Unit"]] = relationship(
        "Unit",
        back_populates="language",
        cascade="all, delete-orphan",
    )

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict =  {
            **super().to_dict(),
            "name": self.name,
            "native_name": self.native_name,
            "level": self.level,
            "description": self.description,
            "flag": self.flag,
            "current_unit": self.current_unit
        }

        if include_relations:
            base_dict.update({
                "unit_ids": [unit.id for unit in self.unit]
            })
        
        return base_dict