from datetime import datetime
from sqlalchemy import JSON, Column, Float, String, ForeignKey, Date

from ...core.database import Base


class StrengthsAndWeaknesses(Base):
    __tablename__ = 'strengths_and_weaknesses'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    language_id = Column(String, ForeignKey('language.id'), nullable=False)
    element_type = Column(String, nullable=False)
    strengths = Column(JSON, default={})
    weaknesses = Column(JSON, default={})
    embeddings = Column(Float, nullable=False)
    created_at = Column(Date, default=datetime.now())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "language_id": self.language_id,
            "element_type": self.element_type,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "embeddings": self.embeddings,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }