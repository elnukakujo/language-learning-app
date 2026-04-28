from sqlalchemy import Column, String, Date, ForeignKey

from ...core.database import Base


class Source(Base):
    __tablename__ = 'source'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    title = Column(String, nullable=False)
    date = Column(Date)
    description = Column(String)
    source_type = Column(String)

