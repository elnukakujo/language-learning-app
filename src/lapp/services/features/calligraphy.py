from datetime import datetime
from typing import Optional

from lapp.utils.helpers import update_difficulty
from sqlalchemy.orm import Session

import logging
logger = logging.getLogger(__name__)

from ...schemas.features import CalligraphyDict
from ...models.features import Calligraphy
from ...core.database import db_manager
from ..containers import LessonService, LanguageService
from ..components import CharacterService, WordService, PassageService
from ...utils import update_score

lesson_service = LessonService()
language_service = LanguageService()
character_service = CharacterService()
passage_service = PassageService()
word_service = WordService()

class CalligraphyService:
    def _serialize(self, calligraphy: Calligraphy | None, as_dict: bool, include_relations: bool) -> Calligraphy | dict | None:
        if not as_dict or calligraphy is None:
            return calligraphy
        return calligraphy.to_dict(include_relations=include_relations)

    def _serialize_list(self, calligraphies: list[Calligraphy], as_dict: bool, include_relations: bool) -> list[Calligraphy] | list[dict]:
        if not as_dict:
            return calligraphies
        return [calligraphy.to_dict(include_relations=include_relations) for calligraphy in calligraphies]

    def get_all(
        self,
        language_id: Optional[str] = None,
        lesson_id: Optional[str] = None,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> list[Calligraphy] | list[dict]:
        """
        Get all calligraphies for a specific language or lesson.

        Args:
            language_id (Optional[str]=None): The id of the language to get all the calligraphies from
            lesson_id (Optional[str]=None): The id of the lesson to get all the calligraphies from
        Returns:
            List of Calligraphy objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and lesson_id), f"language_id and lesson_id can't be both specified, but got: {language_id} and {lesson_id}"
            if language_id:
                lessons = lesson_service.get_all(language_id=language_id, session=session)

                calligraphies = []
                for lesson in lessons:
                    calligraphies.extend(
                        db_manager.find_all(
                            model_class=Calligraphy,
                            filters={'lesson_id': lesson.id},
                            session=session
                        )
                    )
                return self._serialize_list(calligraphies, as_dict, include_relations)
            elif lesson_id:
                calligraphies = db_manager.find_all(
                    model_class=Calligraphy,
                    filters={'lesson_id': lesson_id},
                    session=session
                )
                return self._serialize_list(calligraphies, as_dict, include_relations)
            else:
                raise ValueError(f"Requires either language_id or lesson_id but got: {language_id} and {lesson_id}")
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all calligraphies: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(
        self,
        calligraphy_id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Calligraphy | dict | None:
        """
        Get a Calligraphy item by its ID.

        Args:
            calligraphy_id: The ID of the Calligraphy item to retrieve.

        Returns:
            Calligraphy object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            calligraphy = db_manager.find_by_attr(
                model_class=Calligraphy,
                attr_values={'id': calligraphy_id},
                session=session
            )
            return self._serialize(calligraphy, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get calligraphy by id: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_level(
        self,
        level: str,
        language_id: Optional[str] = None,
        lesson_id: Optional[str] = None,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> list[Calligraphy] | list[dict]:
        """
        Get all Calligraphy items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter Calligraphy items
            lesson_id: The id of the lesson to filter Calligraphy items
            level: Calligraphy level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Calligraphy objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and lesson_id), f"language_id and lesson_id can't be both specified, but got: {language_id} and {lesson_id}"

            if language_id:
                lessons = lesson_service.get_all(language_id=language_id, session=session)

                calligraphies = []
                for lesson in lessons:
                    calligraphies.extend(
                        db_manager.find_all(
                            model_class=Calligraphy,
                            filters={'level':level ,'lesson_id': lesson.id},
                            session=session
                        )
                    )
                return self._serialize_list(calligraphies, as_dict, include_relations)
            elif lesson_id:
                calligraphies = db_manager.find_all(
                    model_class=Calligraphy,
                    filters={'level': level, 'lesson_id': lesson_id},
                    session=session
                )
                return self._serialize_list(calligraphies, as_dict, include_relations)
            else:
                raise ValueError(f"Requires either language_id or lesson_id but got: {language_id} and {lesson_id}")
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get_by_level calligraphies: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    
    def create(
        self,
        data: CalligraphyDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Calligraphy | dict | None:
        """
        Create a new Calligraphy item.

        Args:
            data: CalligraphyDict containing calligraphy item details.

        Returns:
            Created Calligraphy object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            lesson = lesson_service.get_by_id(data.lesson_id, session=session)

            if not lesson:
                logger.warning(f"Cannot create Calligraphy item, lesson not found: {data.lesson_id}")
                return None
            
            # Create Character using CharacterService
            data.character.language_id = lesson.language_id
            character = character_service.create(data.character, session=session)
            if not character:
                logger.error(f"Failed to create character for calligraphy")
                return None
            
            # Ensure character is loaded in session
            if character and not session.get(Calligraphy.character.property.mapper.class_, character.id):
                raise ValueError(f"Character not found in session after creation for calligraphy")
            
            # Create example_word using WordService if provided
            example_word = None
            if data.example_word:
                data.example_word.language_id = lesson.language_id
                example_word = word_service.create(data.example_word, session=session)
                if not example_word:
                    logger.warning(f"Failed to create example_word for calligraphy")
            
            calligraphy = Calligraphy(
                id = db_manager.generate_new_id(
                    model_class=Calligraphy,
                    session=session
                ),
                **{
                    k: v
                    for k, v in data.model_dump(exclude={'character', 'example_word'}, exclude_none=True).items()
                    if k != 'last_seen_at'
                }
            )

            calligraphy.character_id = character.id
            calligraphy.character = character
            calligraphy.example_words = [example_word] if example_word else []
            
            result = db_manager.insert(
                obj=calligraphy,
                session=session
            )

            if result:
                logger.info(f"Created new Calligraphy item with ID: {result.id}")
            else:
                logger.error(f"Failed to create new Calligraphy item")

            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create calligraphy: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(
        self,
        calligraphy_id: str,
        data: CalligraphyDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Calligraphy | dict | None:
        """
        Update an existing Calligraphy item.

        Args:
            calligraphy_id: The ID of the Calligraphy item to update.
            data: calligraphyDict containing updated Calligraphy item details.

        Returns:
            Updated Calligraphy object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(calligraphy_id, session=session)
            
            if not existing:
                logger.warning(f"Calligraphy item not found: {calligraphy_id}")
                return None
            
            # Handle Character update through CharacterService if provided
            if data.character is not None:
                data.character.language_id = existing.character.language_id if existing.character else None
                updated_character = character_service.update(existing.character_id, data.character, session=session)
                if not updated_character:
                    logger.error(f"Failed to update character for calligraphy: {calligraphy_id}")
                    return None
                existing.character = updated_character
            
            # Handle example_word update through WordService if provided
            if data.example_word is not None:
                data.example_word.language_id = existing.character.language_id if existing.character else None
                existing_example_word = existing.example_words[0] if existing.example_words else None
                if existing_example_word:
                    updated_word = word_service.update(existing_example_word.id, data.example_word, session=session)
                    if updated_word:
                        existing.example_words = [updated_word]
                else:
                    new_word = word_service.create(data.example_word, session=session)
                    if new_word:
                        existing.example_words = [new_word]
            else:
                existing.example_words = []
            
            
            # Remove nested objects from update_data
            update_data = data.model_dump()
            update_data.pop('id', None)  # Don't allow updating the ID
            update_data.pop('score', None)  # Don't allow direct score updates
            update_data.pop('difficulty', None)  # Don't allow direct difficulty updates
            update_data.pop('status', None)  # Don't allow direct status updates
            update_data.pop('created_at', None)  # Don't allow updating created_at
            update_data.pop('last_seen_at', None)   # Don't allow direct last_seen_at updates
            
            update_data.pop('character', None)
            update_data.pop('example_word', None)

            # Update the existing object's attributes
            for key, value in update_data.items():
                if key not in ('character_id',):
                    setattr(existing, key, value)
            
            # Save to database
            result = db_manager.modify(existing, session=session)
            
            if result:
                logger.info(f"Updated Calligraphy item: {calligraphy_id}")
            else:
                logger.error(f"Failed to update Calligraphy item: {calligraphy_id}")
            
            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update calligraphy: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, calligraphy_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a Calligraphy item by its ID.

        Args:
            calligraphy_id: The ID of the Calligraphy item to delete.
        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if Calligraphy item exists before deleting
            existing = self.get_by_id(calligraphy_id, session=session)
            
            if not existing:
                logger.warning(f"Calligraphy item not found: {calligraphy_id}")
                return False
            
            # Delete from database
            success = db_manager.delete(existing, session=session)
            
            if success:
                logger.info(f"Deleted Calligraphy item: {calligraphy_id}")
            else:
                logger.error(f"Failed to delete Calligraphy item: {calligraphy_id}")
            
            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete calligraphy: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update_score(
        self,
        calligraphy_id: str,
        score: float,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Calligraphy | dict | None:
        """
        Update Calligraphy item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            calligraphy_id: The ID of the Calligraphy item to update
            score: The new score for the Calligraphy item
        
        Returns:
            Updated Calligraphy object if successful, None otherwise
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            calligraphy = self.get_by_id(calligraphy_id, session=session)

            if not calligraphy:
                logger.warning(f"Calligraphy item not found: {calligraphy_id}")
                return None
            
            previous_score = calligraphy.score

            calligraphy.score = update_score(
                score=calligraphy.score,
                last_seen_at=calligraphy.last_seen_at,
                similarity=score,
            )
            
            calligraphy.difficulty = update_difficulty(
                new_score=score,
                last_seen_at=calligraphy.last_seen_at,
                previous_difficulty=calligraphy.difficulty,
                created_at=calligraphy.created_at
            )

            # Update last_seen_at
            calligraphy.last_seen_at = datetime.now()    
            
            # Save changes
            result = db_manager.modify(calligraphy, session=session)
            
            if result:
                logger.info(f"Updated CalligraphyFeature {calligraphy_id} score to {calligraphy.score} and difficulty to {calligraphy.difficulty}")

            if calligraphy.score != previous_score:
                lesson_service.update_score(calligraphy.lesson_id, session=session)
                logger.info(f"Updated lesson {calligraphy.lesson_id} score due to calligraphy {calligraphy_id}")

                character_service.update_score(char_id=calligraphy.character_id, session=session)
                logger.info(f"Updated character {calligraphy.character_id} score due to calligraphy {calligraphy_id}")

                if calligraphy.example_words:
                    for word in calligraphy.example_words:
                        word_service.update_score(word_id=word.id, session=session)
                        logger.info(f"Updated example word {word.id} score due to calligraphy {calligraphy_id}")
                    
                if calligraphy.example_sentences:
                    for passage in calligraphy.example_sentences:
                        passage_service.update_score(passage_id=passage.id, session=session)
                        logger.info(f"Updated example sentence {passage.id} score due to calligraphy {calligraphy_id}")
            
            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update calligraphy score: {e}")
            raise
        finally:
            if owns_session:
                session.close()
