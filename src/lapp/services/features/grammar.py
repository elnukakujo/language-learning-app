from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

import logging

logger = logging.getLogger(__name__)

from ...schemas.features import GrammarDict
from ...models.features import Grammar
from ..containers import UnitService, LanguageService
from ..components import PassageService
from ...core.database import db_manager
from ...utils import update_score

unit_service = UnitService()
language_service = LanguageService()
passage_service = PassageService()

class GrammarService:
    def get_all(self, language_id: Optional[str] = None, unit_id: Optional[str] = None, session: Optional[Session] = None) -> list[Grammar]:
        """
        Get all Grammar items for a specific language or unit.

        Args:
            language_id (Optional[str] = None): The id of the language to get all the grammars from
            unit_id (Optional[str] = None): The id of the unit to get all the grammars from

        Returns:
            List of Grammar objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"
            if language_id:
                units = unit_service.get_all(language_id=language_id, session=session)

                grammars = []
                for unit in units:
                    grammars.extend(
                        db_manager.find_all(
                            model_class=Grammar,
                            filters={'unit_id': unit.id},
                            session=session
                        )
                    )
                return grammars
            elif unit_id:
                return db_manager.find_all(
                    model_class=Grammar,
                    filters={'unit_id': unit_id},
                    session=session
                )
            else:
                raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all grammars: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(self, grammar_id: str, session: Optional[Session] = None) -> Grammar | None:
        """
        Get a Grammar item by its ID.

        Args:
            grammar_id: The ID of the Grammar item to retrieve.

        Returns:
            Grammar object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_by_attr(
                model_class=Grammar,
                attr_values={'id': grammar_id},
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get grammar by id: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_level(self, level: str, language_id: Optional[str] = None, unit_id: Optional[str] = None, session: Optional[Session] = None) -> list[Grammar]:
        """
        Get all Grammar items of a specific level among a language.
        
        Args:
            language_id: The id of the language to filter Grammar items
            unit_id: The id of the unit to filter Grammar items
            level: Grammar level (e.g., 'A1', 'B2')
        
        Returns:
            List of matching Grammar objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            assert not (language_id and unit_id), f"language_id and unit_id can't be both specified, but got: {language_id} and {unit_id}"

            if language_id:
                units = unit_service.get_all(language_id=language_id, session=session)

                grammars = []
                for unit in units:
                    grammars.extend(
                        db_manager.find_all(
                            model_class=Grammar,
                            filters={'level': level, 'unit_id': unit.id},
                            session=session
                        )
                    )
                return grammars
            elif unit_id:
                return db_manager.find_all(
                    model_class=Grammar,
                    filters={'level': level, 'unit_id': unit_id},
                    session=session
                )
            else:
                raise ValueError(f"Requires either language_id or unit_id but got: {language_id} and {unit_id}")
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get_by_level grammars: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    
    def create(self, data: GrammarDict, session: Optional[Session] = None) -> Grammar | None:
        """
        Create a new Grammar item.

        Args:
            data: GrammarDict containing Grammar item details.

        Returns:
            Created Grammar object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            unit = unit_service.get_by_id(data.unit_id, session=session)

            if not unit:
                logger.warning(f"Cannot create Grammar item, unit not found: {data.unit_id}")
                return None

            # Create Passages using PassageService
            learnable_sentences = []
            for sentence in (data.learnable_sentences or []):
                passage = passage_service.create(sentence, session=session)
                if passage:
                    learnable_sentences.append(passage)

            # Prepare data without learnable_sentences to avoid duplication
            grammar_data = data.model_dump(exclude_none=True)
            grammar_data.pop('learnable_sentences', None)

            grammar = Grammar(
                id = db_manager.generate_new_id(
                    model_class=Grammar,
                    session=session
                ),
                **grammar_data
            )
            
            # Add the passages to the grammar
            grammar.learnable_sentences = learnable_sentences
            
            result = db_manager.insert(
                obj=grammar,
                session=session
            )

            if result:
                logger.info(f"Created new Grammar item with ID: {result.id}")
            else:
                logger.error(f"Failed to create new Grammar item: {grammar.title}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create grammar: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(self, grammar_id: str, data: GrammarDict, session: Optional[Session] = None) -> Grammar | None:
        """
        Update an existing Grammar item.

        Args:
            grammar_id: The ID of the Grammar item to update.
            data: GrammarDict containing updated Grammar item details.

        Returns:
            Updated Grammar object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(grammar_id, session=session)
            
            if not existing:
                logger.warning(f"Grammar item not found: {grammar_id}")
                return None
            
            # Handle learnable_sentences update through PassageService if provided
            if data.learnable_sentences is not None:
                # Delete old passages and create new ones
                for old_passage in existing.learnable_sentences:
                    passage_service.delete(old_passage.id, session=session)
                
                # Create new passages
                new_sentences = []
                for sentence in data.learnable_sentences:
                    passage = passage_service.create(sentence, session=session)
                    if passage:
                        new_sentences.append(passage)
                
                existing.learnable_sentences = new_sentences
            
            # Only update fields that were provided (partial updates)
            update_data = data.model_dump(exclude_unset=True, exclude_none=True)
            
            # Remove nested objects from update_data
            update_data.pop('learnable_sentences', None)
            
            # Update the existing object's attributes
            for key, value in update_data.items():
                setattr(existing, key, value)
            
            # Update last_seen
            existing.last_seen = date.today()
            
            # Save to database
            result = db_manager.modify(existing, session=session)
            
            if result:
                logger.info(f"Updated Grammar item: {grammar_id}")
            else:
                logger.error(f"Failed to update Grammar item: {grammar_id}")
            
            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update grammar: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, grammar_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a Grammar item by its ID.

        Args:
            grammar_id: The ID of the Grammar item to delete.
        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if grammar item exists before deleting
            existing = self.get_by_id(grammar_id, session=session)
            
            if not existing:
                logger.warning(f"Grammar item not found: {grammar_id}")
                return False
            
            # Delete from database
            success = db_manager.delete(existing, session=session)
            
            if success:
                logger.info(f"Deleted Grammar item: {grammar_id}")
            else:
                logger.error(f"Failed to delete Grammar item: {grammar_id}")
            
            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete grammar: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update_score(self, grammar_id: str, success: bool, session: Optional[Session] = None) -> Grammar | None:
        """
        Update Grammar item score based on average of all of its components scores.
        
        This should be called whenever a component's score changes.
        
        Args:
            grammar_id: The ID of the Grammar item to update
            success: Whether the latest attempt was successful
        
        Returns:
            Updated Grammar object if successful, None otherwise
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            grammar = self.get_by_id(grammar_id, session=session)
        
            if not grammar:
                logger.warning(f"Grammar item not found: {grammar_id}")
                return None
            
            previous_score = grammar.score

            grammar.score = update_score(
                current_score=grammar.score,
                last_seen=grammar.last_seen,
                success=success
            )
            
            # Update last_seen
            grammar.last_seen = date.today()

            if grammar.score != previous_score:
                if grammar.unit_id:
                    unit_service.update_score(grammar.unit_id, session=session)
                    logger.info(f"Updated unit {grammar.unit_id} score due to Grammar {grammar_id}")
            
            # Save changes
            result = db_manager.modify(grammar, session=session)
            
            if result:
                logger.info(f"Updated Grammar item {grammar_id} score: {result.score}")
            
            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update grammar score: {e}")
            raise
        finally:
            if owns_session:
                session.close()
