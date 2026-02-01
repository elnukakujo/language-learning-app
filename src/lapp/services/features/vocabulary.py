from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

import logging
logger = logging.getLogger(__name__)

from ...schemas.features import VocabularyDict
from ...models.features import Vocabulary
from ..containers import UnitService, LanguageService
from ..components import WordService, PassageService
from ...core.database import db_manager
from ...utils import update_score

unit_service = UnitService()
language_service = LanguageService()
word_service = WordService()
passage_service = PassageService()


class VocabularyService:
    def get_all(self, language_id: Optional[str] = None, unit_id: Optional[str] = None, session: Optional[Session] = None) -> list[Vocabulary]:
        """
        Get all vocabulary for a specific language or unit.

        Args:
            language_id (Optional[str]): The id of the language to get all the vocabulary from
            unit_id (Optional[str]): The id of the unit to get all the vocabulary from

        Returns:
            List of VocabularyFeature objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"
            if language_id:
                units = unit_service.get_all(language_id=language_id, session=session)

                vocabulary = []
                for unit in units:
                    vocabulary.extend(
                        db_manager.find_all(
                            model_class=Vocabulary,
                            filters={'unit_id': unit.id},
                            session=session
                        )
                    )
                return vocabulary
            elif unit_id:
                return db_manager.find_all(
                    model_class=Vocabulary,
                    filters={'unit_id': unit_id},
                    session=session
                )
            else:
                raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all vocabularies: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(self, voc_id: str, session: Optional[Session] = None) -> Vocabulary | None:
        """
        Get a vocabulary item by its ID.

        Args:
            voc_id: The ID of the vocabulary item to retrieve.

        Returns:
            VocabularyFeature object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_by_attr(
                model_class=Vocabulary,
                attr_values={'id': voc_id},
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get vocabulary by id: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_level(self, language_id: Optional[str], unit_id: Optional[str], level: str, session: Optional[Session] = None) -> list[Vocabulary]:
        """
        Get all vocabulary items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter vocabulary items
            unit_id: The id of the unit to filter vocabulary items
            level: Vocabulary level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching VocabularyFeature objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"

            if language_id:
                units = unit_service.get_all(language_id=language_id, session=session)

                vocabulary = []
                for unit in units:
                    vocabulary.extend(
                        db_manager.find_all(
                            model_class=Vocabulary,
                            filters={'unit_id': unit.id, 'level': level},
                            session=session
                        )
                    )
                return vocabulary
            elif unit_id:
                return db_manager.find_all(
                    model_class=Vocabulary,
                    filters={'level': level, 'unit_id': unit_id},
                    session=session
                )
            else:
                raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get_by_level vocabularies: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    
    def create(self, data: VocabularyDict, session: Optional[Session] = None) -> Vocabulary | None:
        """
        Create a new vocabulary item.

        Args:
            data: VocabularyDict containing vocabulary item details.

        Returns:
            Created VocabularyFeature object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            unit = unit_service.get_by_id(data.unit_id, session=session)

            if not unit:
                logger.warning(f"Cannot create vocabulary item, unit not found: {data.unit_id}")
                return None
            
            word = word_service.create(data.word, session=session)
            if not word:
                logger.error(f"Failed to create word for vocabulary")
                return None

            # Create Passages using PassageService to ensure they're properly persisted
            example_sentences = []
            for example_sentence in (data.example_sentences or []):
                passage = passage_service.create(example_sentence, session=session)
                if passage:
                    example_sentences.append(passage)

            # Create Vocabulary with references to the persisted Word and Passages
            vocabulary = Vocabulary(
                id = db_manager.generate_new_id(
                    model_class=Vocabulary,
                    session=session
                ),
                word_id=word.id,
                unit_id=data.unit_id,
                image_files=data.image_files,
                audio_files=data.audio_files
            )
            
            # Add the passages to the vocabulary
            vocabulary.example_sentences = example_sentences
            
            result = db_manager.insert(
                obj=vocabulary,
                session=session
            )

            if result:
                logger.info(f"Created new VocabularyFeature item with ID: {result.id}")
            else:
                logger.error(f"Failed to create new VocabularyFeature item: {word.word}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create vocabulary: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(self, voc_id: str, data: VocabularyDict, session: Optional[Session] = None) -> Vocabulary | None:
        """
        Update an existing VocabularyFeature item.

        Args:
            voc_id: The ID of the VocabularyFeature item to update.
            data: VocabularyDict containing updated vocabulary item details.

        Returns:
            Updated VocabularyFeature object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(voc_id, session=session)
            
            if not existing:
                logger.warning(f"VocabularyFeature item not found: {voc_id}")
                return None
            
            # Handle Word update through WordService if provided
            if data.word is not None:
                
                if (old_word := word_service.get_by_id(existing.word_id, session=session)):
                    # If word id exists, update that word
                    updated_word = word_service.update(existing.word_id, data.word, session=session)
                    if not updated_word:
                        logger.error(f"Failed to update word for vocabulary: {voc_id}")
                        return None
                    
                    existing.word = updated_word  # Update relationship
                    
                elif (old_word := word_service.get_by_word(data.word.word, session=session)):
                    # If the word already exists, update that word

                    existing_image_files = set(old_word.image_files or [])
                    new_image_files = data.word.image_files or []
                    data.word.image_files = list(existing_image_files | set(new_image_files))

                    existing_audio_files = set(old_word.audio_files or [])
                    new_audio_files = data.word.audio_files or []
                    data.word.audio_files = list(existing_audio_files | set(new_audio_files))

                    updated_word = word_service.update(
                        old_word.id,
                        data.word,
                        session=session
                    )

                    existing.word_id = old_word.id  # Update foreign key
                    existing.word = updated_word  # Update relationship
                else:
                    # Create new word if the referenced one doesn't exist
                    new_word = word_service.create(data.word, session=session)
                    if not new_word:
                        logger.error(f"Failed to create new word for vocabulary: {voc_id}")
                        return None
                    
                    existing.word_id = new_word.id  # Update foreign key
                    existing.word = new_word  # Update relationship
            
            # Handle example_sentences update through PassageService if provided
            if data.example_sentences is not None:
                # Delete old passages and create new ones
                for old_passage in existing.example_sentences:
                    passage_service.delete(old_passage.id, session=session)
                
                # Create new passages
                new_sentences = []
                for example_sentence in data.example_sentences:
                    passage = passage_service.create(example_sentence, session=session)
                    if passage:
                        new_sentences.append(passage)
                
                existing.example_sentences = new_sentences
            
            # Update other fields that were provided (excluding word and example_sentences as they're handled above)
            update_data = data.model_dump(exclude_unset=True, exclude_none=True)
            
            # Remove nested objects from update_data to avoid overwriting our service-managed updates
            update_data.pop('word', None)
            update_data.pop('example_sentences', None)
            
            # Update remaining fields
            for key, value in update_data.items():
                if key != 'word_id':  # Don't overwrite word_id if we already set it
                    setattr(existing, key, value)
            
            # Update last_seen
            existing.last_seen = date.today()
            
            # Save to database
            result = db_manager.modify(existing, session=session)
            
            if result:
                logger.info(f"Updated VocabularyFeature item: {voc_id}")
            else:
                logger.error(f"Failed to update VocabularyFeature item: {voc_id}")
            
            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update vocabulary: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, voc_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a VocabularyFeature item by its ID.

        Args:
            voc_id: The ID of the VocabularyFeature item to delete.

        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if vocabulary item exists before deleting
            existing = self.get_by_id(voc_id, session=session)
            
            if not existing:
                logger.warning(f"VocabularyFeature item not found: {voc_id}")
                return False
            
            # Delete from database
            success = db_manager.delete(existing, session=session)
            
            if success:
                logger.info(f"Deleted VocabularyFeature item: {voc_id}")
            else:
                logger.error(f"Failed to delete VocabularyFeature item: {voc_id}")
            
            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update vocabulary: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update_score(self, voc_id: str, success: bool, session: Optional[Session] = None) -> Vocabulary | None:
        """
        Update VocabularyFeature item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            voc_id: The ID of the VocabularyFeature item to update
            success: Whether the latest attempt was successful
        
        Returns:
            Updated VocabularyFeature object if successful, None otherwise
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            vocabulary = self.get_by_id(voc_id, session=session)
            
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
            result = db_manager.modify(vocabulary, session=session)

            if result:
                logger.info(f"Updated VocabularyFeature item {voc_id} score: {result.score}")

            if vocabulary.score != previous_score:
                if vocabulary.unit_id:
                    unit_service.update_score(vocabulary.unit_id, session=session)
                    logger.info(f"Updated unit {vocabulary.unit_id} score due to VocabularyFeature {voc_id}")
            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update vocabulary: {e}")
            raise
        finally:
            if owns_session:
                session.close()
