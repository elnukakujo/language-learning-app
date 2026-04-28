from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Date

from ...core.database import Base


class StrengthsAndWeaknesses(Base):
    __tablename__ = 'strengths_and_weaknesses'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    language_id = Column(String, ForeignKey('language.id'), nullable=False)
    language_name = Column(String, nullable=False)
    element_type = Column(String, nullable=False)
    strengths = Column(String, default='')
    weaknesses = Column(String, default='')
    last_updated = Column(Date, default=datetime.now())

