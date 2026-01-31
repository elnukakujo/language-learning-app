from datetime import date
from typing import Optional

import logging
logger = logging.getLogger(__name__)

from ..schemas.features import VocabularyDict
from ..models.features import Vocabulary
from ..models.components import Word, Passage
from . import UnitService, LanguageService
from ..core.database import db_manager
from ..utils import update_score

unit_service = UnitService()
language_service = LanguageService()


class VocabularyService:
    def get_all(self, language_id: Optional[str] = None , unit_id: Optional[str] = None) -> list[Vocabulary]:
        """
        Get all vocabulary for a specific language or unit.

        Args:
            language_id (Optional[str]): The id of the language to get all the vocabulary from
            unit_id (Optional[str]): The id of the unit to get all the vocabulary from

        Returns:
            List of VocabularyFeature objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"
        if language_id:
            units = unit_service.get_all(language_id=language_id)

            vocabulary = []
            for unit in units:
                vocabulary.extend(
                    db_manager.find_all(
                        model_class=Vocabulary,
                        filters={'unit_id': unit.id}
                    )
                )
            return vocabulary
        elif unit_id:
            return db_manager.find_all(
                model_class=Vocabulary,
                filters={'unit_id': unit_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")

    def get_by_id(self, voc_id:str) -> Vocabulary | None:
        """
        Get a vocabulary item by its ID.

        Args:
            voc_id: The ID of the vocabulary item to retrieve.

        Returns:
            VocabularyFeature object if found, else None
        """
        return db_manager.find_by_attr(
            model_class=Vocabulary,
            attr_values={'id': voc_id}
        )

    def get_by_level(self, language_id: Optional[str], unit_id: Optional[str], level: str) -> list[Vocabulary]:
        """
        Get all vocabulary items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter vocabulary items
            unit_id: The id of the unit to filter vocabulary items
            level: Vocabulary level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching VocabularyFeature objects
        """
        assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"

        if language_id:
            units = unit_service.get_all(language_id=language_id)

            vocabulary = []
            for unit in units:
                vocabulary.extend(
                    db_manager.find_all(
                        model_class=Vocabulary,
                        filters={'unit_id': unit.id, 'level': level}
                    )
                )
            return vocabulary
        elif unit_id:
            return db_manager.find_all(
                model_class=Vocabulary,
                filters={'level': level, 'unit_id': unit_id}
            )
        else:
            raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
    
    def create(self, data: VocabularyDict) -> Vocabulary | None:
        """
        Create a new vocabulary item.

        Args:
            data: VocabularyDict containing vocabulary item details.

        Returns:
            Created VocabularyFeature object if successful, else None
        """
        unit = unit_service.get_by_id(data.unit_id)

        if not unit:
            logger.warning(f"Cannot create vocabulary item, unit not found: {data.unit_id}")
            return None
        
        word = Word(
            id = db_manager.generate_new_id(
                model_class=Word
            ),
            **data.word.model_dump(exclude_none=True)
        )

        example_sentences = []
        for _, example_sentence in enumerate(data.example_sentences or []):
            passage = Passage(
                id = db_manager.generate_new_id(
                    model_class=Passage
                ),
                **example_sentence.model_dump(exclude_none=True)
            )
            example_sentences.append(passage)

        vocabulary = Vocabulary(
            id = db_manager.generate_new_id(
                model_class=Vocabulary
            ),
            word=word,
            example_sentences=example_sentences,
            unit_id=data.unit_id,
            image_files=data.image_files,
            audio_files=data.audio_files
        )
        result = db_manager.insert(
            obj=vocabulary
        )

        if result:
            logger.info(f"Created new VocabularyFeature item with ID: {result.id}")
        else:
            logger.error(f"Failed to create new VocabularyFeature item: {vocabulary.word}")

        return result

    def update(self, voc_id: str, data: VocabularyDict) -> Vocabulary | None:
        """
        Update an existing VocabularyFeature item.

        Args:
            voc_id: The ID of the VocabularyFeature item to update.
            data: VocabularyDict containing updated vocabulary item details.

        Returns:
            Updated VocabularyFeature object if successful, else None
        """
        existing = self.get_by_id(voc_id)
        
        if not existing:
            logger.warning(f"VocabularyFeature item not found: {voc_id}")
            return None
        
        # Only update fields that were provided (partial updates)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        
        # Update the existing object's attributes
        for key, value in update_data.items():
            setattr(existing, key, value)
        
        # Update last_seen
        existing.last_seen = date.today()
        
        # Save to database
        result = db_manager.modify(existing)
        
        if result:
            logger.info(f"Updated VocabularyFeature item: {voc_id}")
        else:
            logger.error(f"Failed to update VocabularyFeature item: {voc_id}")
        
        return result

    def delete(self, voc_id: str) -> bool:
        """
        Delete a VocabularyFeature item by its ID.

        Args:
            voc_id: The ID of the VocabularyFeature item to delete.

        Returns:
            True if deletion was successful, else False
        """
        # Check if vocabulary item exists before deleting
        existing = self.get_by_id(voc_id)
        
        if not existing:
            logger.warning(f"VocabularyFeature item not found: {voc_id}")
            return False
        
        # Delete from database
        success = db_manager.delete(existing)
        
        if success:
            logger.info(f"Deleted VocabularyFeature item: {voc_id}")
        else:
            logger.error(f"Failed to delete VocabularyFeature item: {voc_id}")
        
        return success

    def update_score(self, voc_id: str, success: bool) -> Vocabulary | None:
        """
        Update VocabularyFeature item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            voc_id: The ID of the VocabularyFeature item to update
            success: Whether the latest attempt was successful
        
        Returns:
            Updated VocabularyFeature object if successful, None otherwise
        """
        vocabulary = self.get_by_id(voc_id)
        
        if not vocabulary:
            logger.warning(f"VocabularyFeature item not found: {voc_id}")
            return None
        
        previous_score = vocabulary.score
        
        vocabulary.score = update_score(
            score=vocabulary.score,
            last_seen=vocabulary.last_seen,
            success=success
        )

        # Update last_seen
        vocabulary.last_seen = date.today()
        
        # Save changes
        result = db_manager.modify(vocabulary)

        if result:
            logger.info(f"Updated VocabularyFeature item {voc_id} score: {result.score}")

        if vocabulary.score != previous_score:
            if vocabulary.unit_id:
                unit_service.update_score(vocabulary.unit_id)
                logger.info(f"Updated unit {vocabulary.unit_id} score due to VocabularyFeature {voc_id}")
            if vocabulary.language_id:
                language_service.update_score(vocabulary.language_id)
                logger.info(f"Updated language {vocabulary.language_id} score due to VocabularyFeature {voc_id}")
        
        return result