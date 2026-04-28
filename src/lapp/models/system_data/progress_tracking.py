from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer

from ...core.database import Base


class ProgressTracking(Base):
    __tablename__ = 'progress_tracking'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    language_id = Column(String, ForeignKey('language.id'), nullable=False)
    language_name = Column(String, nullable=False)
    element_type = Column(String, nullable=False)
    element_status = Column(String, nullable=False)
    new_score_difference = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    n_reviewed = Column(Integer, nullable=False, default=1)

