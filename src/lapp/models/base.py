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

class BaseContainerModel(Base):
    """
    Base class for models that are containers for other models.
    This includes: Unit, Language
    """
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
    
class BaseFeatureModel(BaseContainerModel):
    """
    Base class for components that belong to both a Unit and a Language.
    This includes: Vocabulary, Grammar, Calligraphy, Exercise
    """
    __abstract__ = True
    
    # Foreign keys - shared by all components
    unit_id: Mapped[str] = mapped_column(ForeignKey("unit.id"))
    
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
    
    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(),
            "image_files": self.image_files,
            "audio_files": self.audio_files
        }
        
        if include_relations:
            base_dict.update({
                "unit_id": self.unit_id
            })
        
        return base_dict
    
    @validates('image_files', 'audio_files')
    def validate_media_files(cls, value: Any, info) -> list[str]:
        """Validate and filter media file paths."""
        if info is None or not isinstance(info, list):
            return []

        media_root = Path(current_app.config['MEDIA_ROOT']).resolve()
        valid_files = []

        for file_path in info:
            if not isinstance(file_path, str):
                logger.warning(f"Invalid media file path (not a string): {file_path}")
                continue

            normalized_path = file_path.replace('\\', '/')

            if value == "image_files" and not normalized_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                logger.warning(f"Invalid image file extension: {normalized_path}")
                continue
            if value == "audio_files" and not normalized_path.lower().endswith(('.mp3', '.wav', '.ogg', '.flac', '.m4a')):
                logger.warning(f"Invalid audio file extension: {normalized_path}")
                continue

            if normalized_path.lower().startswith('/media/images/') or normalized_path.lower().startswith('/media/audio/'):
                relative_path = normalized_path[len('/media/'):]
            elif normalized_path.lower().startswith('/media_dev/images/') or normalized_path.lower().startswith('/media_dev/audio/'):
                relative_path = normalized_path[len('/media_dev/'):]
            elif normalized_path.lower().startswith('/media_test/images/') or normalized_path.lower().startswith('/media_test/audio/'):
                relative_path = normalized_path[len('/media_test/'):]
            elif normalized_path.lower().startswith('images/') or normalized_path.lower().startswith('audio/'):
                relative_path = normalized_path
            else:
                logger.warning(f"Invalid media URL prefix: {normalized_path}")
                continue

            try:
                full_path = (media_root / relative_path).resolve()
                full_path.relative_to(media_root)
            except Exception:
                logger.warning(f"Media path escapes MEDIA_ROOT: {normalized_path}")
                continue

            if full_path.exists() and full_path.is_file():
                valid_files.append(normalized_path)

        return valid_files
    
class BaseComponentModel(Base):
    """
    Base class for components models.
    This includes: Calligraphy, Word, and Passage
    """
    __abstract__ = True

    id = Column(String, primary_key=True, index=True)

    # Media files
    image_files = Column(JSON, default=list)
    audio_files = Column(JSON, default=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "image_files": self.image_files,
            "audio_files": self.audio_files
        }
    
    @validates('image_files', 'audio_files')
    def validate_media_files(cls, value: Any, info) -> list[str]:
        """Validate and filter media file paths."""
        if info is None or not isinstance(info, list):
            return []

        media_root = Path(current_app.config['MEDIA_ROOT']).resolve()
        valid_files = []

        for file_path in info:
            if not isinstance(file_path, str):
                logger.warning(f"Invalid media file path (not a string): {file_path}")
                continue

            normalized_path = file_path.replace('\\', '/')

            if value == "image_files" and not normalized_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                logger.warning(f"Invalid image file extension: {normalized_path}")
                continue
            if value == "audio_files" and not normalized_path.lower().endswith(('.mp3', '.wav', '.ogg', '.flac', '.m4a')):
                logger.warning(f"Invalid audio file extension: {normalized_path}")
                continue

            if normalized_path.lower().startswith('/media/images/') or normalized_path.lower().startswith('/media/audio/'):
                relative_path = normalized_path[len('/media/'):]
            elif normalized_path.lower().startswith('/media_dev/images/') or normalized_path.lower().startswith('/media_dev/audio/'):
                relative_path = normalized_path[len('/media_dev/'):]
            elif normalized_path.lower().startswith('/media_test/images/') or normalized_path.lower().startswith('/media_test/audio/'):
                relative_path = normalized_path[len('/media_test/'):]
            elif normalized_path.lower().startswith('images/') or normalized_path.lower().startswith('audio/'):
                relative_path = normalized_path
            else:
                logger.warning(f"Invalid media URL prefix: {normalized_path}")
                continue

            try:
                full_path = (media_root / relative_path).resolve()
                full_path.relative_to(media_root)
            except Exception:
                logger.warning(f"Media path escapes MEDIA_ROOT: {normalized_path}")
                continue

            if full_path.exists() and full_path.is_file():
                valid_files.append(normalized_path)

        return valid_files