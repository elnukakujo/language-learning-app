from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from ...core.database import Base


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    tagged_element_type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String)
    description = Column(String)

