from datetime import date
from typing import Optional
from sqlalchemy.orm import Session

import logging
logger = logging.getLogger(__name__)

from ...schemas.containers import LanguageDict
from ...models.containers import Language, Unit
from ...core.database import db_manager

class LanguageService:
    def _serialize(self, language: Language | None, as_dict: bool, include_relations: bool) -> Language | dict | None:
        if not as_dict or language is None:
            return language
        return language.to_dict(include_relations=include_relations)

    def _serialize_list(self, languages: list[Language], as_dict: bool, include_relations: bool) -> list[Language] | list[dict]:
        if not as_dict:
            return languages
        return [language.to_dict(include_relations=include_relations) for language in languages]

    def _check_current_unit(self, language: Language, current_unit_id: str, session: Optional[Session] = None) -> bool:
        """
        Check if the current unit ID is valid for the given language.

        Args:
            language: The Language object.
            current_unit_id: The current unit ID to validate.
        Returns:
            True if valid, False otherwise.
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            from .unit import UnitService
            unit_service = UnitService()
            if (unit := unit_service.get_by_id(current_unit_id, session=session)):
                return unit.id
            new_current_unit_id = self._find_current_unit(language.id, score_threshold=0.75, session=session)

            language.current_unit = new_current_unit_id
            db_manager.modify(language, session=session)
            return new_current_unit_id
            
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to check current unit {current_unit_id} for language {language.id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    
    def _find_current_unit(self, language_id: str, score_threshold: float, session: Optional[Session] = None) -> Optional[str]:
        """
        Find the first unit ID for a given language with a score below a certain threshold.

        Args:
            language_id: The ID of the language.
            score_threshold: The score threshold to compare against.
            session: Optional SQLAlchemy session.
        
        Returns:
            The ID of the first unit below the threshold, or None if all units meet/exceed the threshold.
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            from .unit import UnitService
            unit_service = UnitService()

            units = unit_service.get_all(
                language_id=language_id,
                session=session
            )
            for unit in units:
                if unit.score < score_threshold*100:
                    return unit.id
            return units[-1].id if units else None
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to find current unit for language {language_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
        
    def get_all(
        self,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> list[Language] | list[dict]:
        """
        Get all languages.

        Args:
            None

        Returns:
            List of Language objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            languages = db_manager.find_all(
                model_class=Language,
                session=session
            )
            for language in languages:
                # Ensure current_unit is valid
                language.current_unit = self._check_current_unit(
                    language=language,
                    current_unit_id=language.current_unit,
                    session=session
                )
            return self._serialize_list(languages, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all languages: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(
        self,
        language_id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Language | dict | None:
        """
        Get a language by its ID.

        Args:
            language_id: The ID of the language to retrieve.

        Returns:
            Language object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            language = db_manager.find_by_attr(
                model_class=Language,
                attr_values={'id': language_id},
                session=session
            )
            if language:
                language.current_unit = self._check_current_unit(
                    language=language,
                    current_unit_id=language.current_unit,
                    session=session
                )
            return self._serialize(language, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get language {language_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_level(
        self,
        level: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> list[Language] | list[dict]:
        """
        Get all languages of a specific level.
        
        Args:
            level: Language level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Language objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            languages = db_manager.find_all(
                model_class=Language,
                filters={'level': level},
                session=session
            )
            for language in languages:
                # Ensure current_unit is valid
                language.current_unit = self._check_current_unit(
                    language=language,
                    current_unit_id=language.current_unit,
                    session=session
                )
            return self._serialize_list(languages, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get languages by level {level}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    
    def create(
        self,
        data: LanguageDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Language | dict | None:
        """
        Create a new language.

        Args:
            data: LanguageDict containing language details.

        Returns:
            Created Language object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            language = Language(
                id = db_manager.generate_new_id(model_class=Language, session=session),
                **data.model_dump(exclude_none=True)
            )

            language.last_seen = date.today()
            language.score = 0.0
            language.current_unit = self._find_current_unit(
                language_id=language.id,
                score_threshold=0.75,
                session=session
            )

            result = db_manager.insert(
                obj=language,
                session=session
            )

            if result:
                logger.info(f"Created new language with ID: {result.id}")
            else:
                logger.error(f"Failed to create new language: {language.name}")

            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create language: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(
        self,
        language_id: str,
        data: LanguageDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True
    ) -> Language | dict | None:
        """
        Update an existing language.

        Args:
            language_id: The ID of the language to update.
            data: LanguageDict containing updated language details.

        Returns:
            Updated Language object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(language_id, session=session)
            
            if not existing:
                logger.warning(f"Language not found: {language_id}")
                return None
            
            # Only update fields that were provided (partial updates)
            update_data = data.model_dump(exclude_unset=True, exclude_none=True)
            
            # Update the existing object's attributes
            for key, value in update_data.items():
                setattr(existing, key, value)
            
            # Update last_seen
            existing.last_seen = date.today()
            existing.current_unit = self._check_current_unit(
                language=existing,
                current_unit_id=existing.current_unit,
                session=session
            )
            
            # Save to database
            result = db_manager.modify(existing, session=session)
            
            if result:
                logger.info(f"Updated language: {language_id}")
            else:
                logger.error(f"Failed to update language: {language_id}")
            
            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update language {language_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, language_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a language by its ID.

        Args:
            language_id: The ID of the language to delete.

        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if language exists before deleting
            existing = self.get_by_id(language_id, session=session)
            
            if not existing:
                logger.warning(f"Language not found: {language_id}")
                return False
            
            # Delete from database
            success = db_manager.delete(existing, session=session)
            
            if success:
                logger.info(f"Deleted language: {language_id}")
            else:
                logger.error(f"Failed to delete language: {language_id}")
            
            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete language {language_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update_score(self, language_id: str, session: Optional[Session] = None) -> Language | None:
        """
        Update language score based on average of all unit scores.
        
        This should be called whenever a unit's score changes.
        
        Args:
            language_id: The ID of the language to update
        
        Returns:
            Updated Language object if successful, None otherwise
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            language = self.get_by_id(language_id, session=session)
            
            if not language:
                logger.warning(f"Language not found: {language_id}")
                return None
            
            # Get all units for this language
            units = db_manager.find_all(
                model_class=Unit,
                filters={'language_id': language_id},
                session=session
            )
            
            if not units:
                logger.warning(f"No units found for language: {language_id}")
                language.score = 0.0
            else:
                # Calculate average score from all units
                total_score = sum(unit.score for unit in units)
                language.score = round(total_score / len(units), 2)
                
                logger.info(
                    f"Calculated language score: {language.score} "
                    f"(from {len(units)} units)"
                )
            
            # Update last_seen
            language.last_seen = date.today()
            language.current_unit = self._find_current_unit(
                language_id=language.id,
                score_threshold=0.75,
                session=session
            )
            
            # Save changes
            result = db_manager.modify(language, session=session)
            
            if result:
                logger.info(f"Updated language {language_id} score: {result.score}")
            
            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update language score for {language_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
