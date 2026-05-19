from flask import current_app
from typing import Any, List
from pathlib import Path
from sqlalchemy import Column, Float, String, Integer, DateTime, JSON, ForeignKey, Table, Computed, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr, validates
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

from ..core.database import Base

# Feature link tables introduced by the lesson migration.
vocabulary_example_sentence_link = Table(
    "vocabulary_example_sentence",
    Base.metadata,
    Column("vocabulary_id", String, ForeignKey("vocabulary.id"), primary_key=True),
    Column("passage_id", String, ForeignKey("passage.id"), primary_key=True),
)

grammar_example_word_link = Table(
    "grammar_example_word",
    Base.metadata,
    Column("grammar_id", String, ForeignKey("grammar.id"), primary_key=True),
    Column("word_id", String, ForeignKey("word.id"), primary_key=True),
)

grammar_example_sentence_link = Table(
    "grammar_example_sentence",
    Base.metadata,
    Column("grammar_id", String, ForeignKey("grammar.id"), primary_key=True),
    Column("passage_id", String, ForeignKey("passage.id"), primary_key=True),
)

calligraphy_example_word_link = Table(
    "calligraphy_example_word",
    Base.metadata,
    Column("calligraphy_id", String, ForeignKey("calligraphy.id"), primary_key=True),
    Column("word_id", String, ForeignKey("word.id"), primary_key=True),
)
calligraphy_example_sentence_link = Table(
    "calligraphy_example_sentence",
    Base.metadata,
    Column("calligraphy_id", String, ForeignKey("calligraphy.id"), primary_key=True),
    Column("passage_id", String, ForeignKey("passage.id"), primary_key=True),
)

exercise_vocabulary_link = Table(
    "exercise_vocabulary_link",
    Base.metadata,
    Column("exercise_id", String, ForeignKey("exercise.id"), primary_key=True),
    Column("vocabulary_id", String, ForeignKey("vocabulary.id"), primary_key=True),
)

exercise_grammar_link = Table(
    "exercise_grammar_link",
    Base.metadata,
    Column("exercise_id", String, ForeignKey("exercise.id"), primary_key=True),
    Column("grammar_id", String, ForeignKey("grammar.id"), primary_key=True),
)

exercise_calligraphy_link = Table(
    "exercise_calligraphy_link",
    Base.metadata,
    Column("exercise_id", String, ForeignKey("exercise.id"), primary_key=True),
    Column("calligraphy_id", String, ForeignKey("calligraphy.id"), primary_key=True),
)

# --- Association tables (polymorphic, no FK on element_id) ---

source_element_link = Table(
    "source_element_link", Base.metadata,
    Column("source_id", String, ForeignKey("source.id"), nullable=False),
    Column("element_id", String, nullable=False),
    PrimaryKeyConstraint("source_id", "element_id")
)

tag_element_link = Table(
    "tag_element_link", Base.metadata,
    Column("tag_id", String, ForeignKey("tag.id"), nullable=False),
    Column("element_id", String, nullable=False),
    PrimaryKeyConstraint("tag_id", "element_id")
)


class BaseElementModel(Base):
    """
    Base class for all models that represent individual elements.
    This includes: Word, Passage, and Calligraphy
    """
    __abstract__ = True

    id = Column(String, primary_key=True, index=True)
    score = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    last_seen_at = Column("last_seen_at", DateTime, default=datetime.now, nullable=True)
    status = Column(
        String, 
        Computed("CASE WHEN score = 0 THEN 'unstarted' WHEN score <= 30 THEN 'beginner' WHEN score <= 60 THEN 'intermediary' WHEN score <= 90 THEN 'advanced' ELSE 'fluent' END"),
        nullable=False
    )

    @declared_attr
    def tags(cls) -> Mapped[List["Tag"]]:
        from .system_data import Tag
        return relationship(
            "Tag",
            secondary=tag_element_link,
            primaryjoin=cls.id == tag_element_link.c.element_id,
            secondaryjoin=tag_element_link.c.tag_id == Tag.id,
            viewonly=False,
            overlaps="tags",
        )

    @declared_attr
    def sources(cls) -> Mapped[List["Source"]]:
        from .system_data import Source
        return relationship(
            "Source",
            secondary=source_element_link,
            primaryjoin=cls.id == source_element_link.c.element_id,
            secondaryjoin=source_element_link.c.source_id == Source.id,
            viewonly=False,
            overlaps="sources",
        )
    
    def get_progress_tracking(self):
        """Retrieve all ProgressTracking entries linked to this element."""
        from ..models.data_collection import ProgressTracking
        from ..core.database import db_manager
        
        return db_manager.find_by_attr(ProgressTracking, {"element_id": self.id})
    
    def get_score_history(self):
        """Retrieve all ProgressTracking entries linked to this element."""
        from ..models.data_collection import ScoreHistory
        from ..core.database import db_manager
        
        return db_manager.find_by_attr(ScoreHistory, {"element_id": self.id})

    def to_dict(self, include_relations: bool = True) -> dict:
        # Allow cooperative multiple-inheritance: call next to_dict in MRO
        parent_to_dict = getattr(super(), "to_dict", None)
        base = parent_to_dict(include_relations=include_relations) if callable(parent_to_dict) else {}

        base.update({
            "id": self.id,
            "score": self.score,
            "created_at": self.created_at.isoformat(),
            "last_seen_at": self.last_seen_at.isoformat() if self.last_seen_at else None,
            "status": self.status
        })

        if include_relations:
            base.update({
                "tags": [tag.to_dict(include_relations=False) for tag in self.tags],
                "sources": [source.to_dict(include_relations=False) for source in self.sources],
                "progress_tracking": [pt.to_dict(include_relations=False) for pt in self.get_progress_tracking()],
                "score_history": [sh.to_dict(include_relations=False) for sh in self.get_score_history()]
            })

        return base
    
class BaseModelWithMediaFiles(Base):
    """
    Base class for models that can have media files.
    This includes: Word, Passage, Calligraphy, Vocabulary, Grammar, Exercise
    """
    __abstract__ = True

    image_files = Column(JSON, default=list)
    audio_files = Column(JSON, default=list)

    def to_dict(self, include_relations: bool = True) -> dict:
        return {
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
    
class BaseContainerModel(BaseElementModel):
    """
    Base class for models that are containers for other models.
    This includes: Lesson, Language
    """
    __abstract__ = True
    
    level = Column(String)
    description = Column(String, default="")

    # Foreign key
    user_id = Column(String, ForeignKey('user.id'), default="user_U0")

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(include_relations=include_relations),
            "level": self.level,
            "description": self.description
        }

        if include_relations:
            base_dict.update({
                "user_id": self.user_id
            })
        return base_dict
    
    
class BaseFeatureModel(BaseElementModel, BaseModelWithMediaFiles):
    """
    Base class for features that belong to a lesson.
    This includes: Vocabulary, Grammar, Calligraphy, Exercise
    """
    __abstract__ = True

    difficulty = Column(Float, default=0.5)
    
    # Foreign keys - shared by all components
    lesson_id: Mapped[str] = mapped_column("lesson_id", ForeignKey("lesson.id"))
    
    # Relationships - use declared_attr to dynamically create for each subclass
    @declared_attr
    def lesson(cls) -> Mapped["Lesson"]:
        """Relationship to parent Lesson. Each subclass gets its own."""
        return relationship(
            "Lesson",
            back_populates=cls.__tablename__
        )
    
    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(include_relations=include_relations),
            "difficulty": self.difficulty
        }
        
        if include_relations:
            base_dict.update({
                "lesson_id": self.lesson_id,
            })
        
        return base_dict
    
class BaseComponentModel(BaseElementModel, BaseModelWithMediaFiles):
    """
    Base class for components models.
    This includes: Calligraphy, Word, and Passage
    """
    __abstract__ = True

    difficulty = Column(Float, default=0.5)

    # Foreign keys 
    language_id: Mapped[str] = mapped_column(ForeignKey("language.id"), nullable=False)

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            **super().to_dict(include_relations=include_relations),
            "difficulty": self.difficulty
        }
        
        if include_relations:
            base_dict.update({
                "language_id": self.language_id,
            })
        
        return base_dict
    
class BaseDataCollectionModel(Base):
    """
    Base class for models that are used for data collection and user-specific data.
    This includes: User, UserPreferences, Source, Tag, StrengthsAndWeaknesses, ProgressTracking
    """
    __abstract__ = True

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now, nullable=True)

    # Foreign keys - commonly used in data collection models
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    language_id = Column(String, ForeignKey('language.id'), nullable=False)

    def to_dict(self, include_relations: bool = True) -> dict:
        base_dict = {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id,
            "language_id": self.language_id
        }
        return base_dict