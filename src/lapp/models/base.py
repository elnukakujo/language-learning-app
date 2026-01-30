import os
from flask import current_app
from typing import Any
from pathlib import Path
from sqlalchemy import Column, String, Integer, Date, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr, validates
from datetime import date

import logging
logger = logging.getLogger(__name__)

from ..core.database import Base

class BaseModel(Base):
    __abstract__ = True

    id = Column(String, primary_key=True, index=True)
    score = Column(Integer, default=0)  # e.g., how much the vocabulary is mastered
    last_seen = Column(Date, default=date.today)  # e.g., when the vocabulary was last seen

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "score": self.score,
            "last_seen": self.last_seen.isoformat(),
        }
    
class BaseComponentModel(BaseModel):
    """
    Base class for components that belong to both a Unit and a Language.
    This includes: Vocabulary, Grammar, Character, Exercise
    """
    __abstract__ = True
    
    # Foreign keys - shared by all components
    unit_id: Mapped[str] = mapped_column(ForeignKey("unit.id"))
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"))
    
    # Media files
    image_files = Column(JSON, default=list)
    audio_files = Column(JSON, default=list)
    
    # Relationships - use declared_attr to dynamically create for each subclass
    @declared_attr
    def unit(cls) -> Mapped["Unit"]:
        """Relationship to parent Unit. Each subclass gets its own."""
        # Get the table name to determine the back_populates name
        
        return relationship(
            "Unit",
            back_populates=cls.__tablename__
        )
    
    @declared_attr
    def language(cls) -> Mapped["Language"]:
        """Relationship to parent Language. Each subclass gets its own."""        
        return relationship(
            "Language",
            back_populates=cls.__tablename__
        )
    
    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(),
            "image_files": self.image_files,
            "audio_files": self.audio_files
        }
        
        if include_relations:
            base_dict.update({
                "unit_id": self.unit_id,
                "language_id": self.language_id
            })
        
        return base_dict
    
    @validates('image_files', 'audio_files')
    def validate_media_files(cls, value: Any, info) -> list[str]:
        """Validate and filter media file paths."""
        # Ensure it's a list
        if info is None or not isinstance(info, list):
            return []
        
        # Get media root from Flask config
        media_root = Path(current_app.config['MEDIA_ROOT'])
        
        # Filter valid files
        valid_files = []
        for file_path in info:
            if not isinstance(file_path, str):
                logger.warning(f"Invalid media file path (not a string): {file_path}")
                continue

            if value == "image_files" and not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                logger.warning(f"Invalid image file extension: {file_path}")
                continue
            elif value == "image_files" and not file_path.lower().startswith('/images/'):
                logger.warning(f"Image file path must start with '/images/': {file_path}")
                continue

            if value == "audio_files" and not file_path.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                logger.warning(f"Invalid audio file extension: {file_path}")
                continue
            elif value == "audio_files" and not file_path.lower().startswith('/audio/'):
                logger.warning(f"Audio file path must start with '/audio/': {file_path}")
                continue
            
            # Check if file exists in media root
            full_path = Path(os.path.join(media_root, file_path.lstrip('/')))
            if full_path.exists() and full_path.is_file():
                valid_files.append(file_path)
        
        return valid_files