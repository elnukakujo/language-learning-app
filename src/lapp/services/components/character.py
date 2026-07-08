import logging
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from ...schemas.components import CharacterDict
from ...models.components import Character
from ...models.containers import Language
from ...core.database import db_manager
from ...models.system_data import Tag, Source
from ...utils import enrich_character, get_language_by_iso2t

class CharacterService:
    def get_all(self, session: Optional[Session] = None) -> list[Character]:
        """
        Get all characters.

        Args:
            None

        Returns:
            List of Character objects
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_all(
                model_class=Character,
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all characters: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(self, character_id: str, session: Optional[Session] = None) -> Character | None:
        """
        Get a character by its ID.

        Args:
            character_id: The ID of the character to retrieve.

        Returns:
            Character object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            return db_manager.find_by_attr(
                model_class=Character,
                attr_values={'id': character_id},
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get character {character_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_character(self, character: str, language_id: Optional[str] = None, session: Optional[Session] = None) -> Character | None:
        """
        Get a character by its character value.

        Args:
            character: The character string to retrieve.

        Returns:
            Character object if found, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            filters = {'character': character}
            if language_id:
                filters['language_id'] = language_id
            return db_manager.find_by_attr(
                model_class=Character,
                attr_values=filters,
                session=session
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get character by character value '{character}': {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def create(self, data: CharacterDict, session: Optional[Session] = None) -> Character | None:
        """
        Create a new character.

        Args:
            data: CharacterDict containing character details.

        Returns:
            Created Character object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            if existing := self.get_by_character(data.character, language_id=data.language_id, session=session):
                logger.info(f"Character already exists: {data.character} with ID: {existing.id}")
                existing = self.update(character_id=existing.id, data=data, session=session)
                existing = session.merge(existing)
                return existing
            
            language = db_manager.find_by_attr(model_class=Language, attr_values={"id": data.language_id}, session=session)

            source_iso1 = get_language_by_iso2t(language.source_iso639_2t).iso1 if language else None
            target_iso1 = get_language_by_iso2t(language.target_iso639_2t).iso1 if language else None

            enriched_data = enrich_character(character_text=data.character, target_iso1=target_iso1, source_iso1=source_iso1)
            
            character = Character(
                id=db_manager.generate_new_id(model_class=Character, session=session),
                **{k: v for k, v in data.model_dump(exclude={'id', 'status', 'score', 'created_at', 'last_seen_at', 'phonetic', 'radical', 'meaning'}, exclude_none=True).items()},
                phonetic=data.phonetic if (data.phonetic is not None and data.phonetic != "") else enriched_data["phonetic"],
                radical=data.radical if (data.radical is not None and data.radical != "") else enriched_data["radical"],
                meaning=data.meaning if (data.meaning is not None and data.meaning != "") else enriched_data["meaning"],
                tags = session.query(Tag).filter(Tag.id.in_([t.id for t in data.tags])).all() if data.tags else [],
                sources = session.query(Source).filter(Source.id.in_([s.id for s in data.sources])).all() if data.sources else []
            )
            result = db_manager.insert(obj=character, session=session)

            if result:
                logger.info(f"Created new character with ID: {result.id}")
            else:
                logger.error(f"Failed to create new character: {character.character}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create character: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(self, character_id: str, data: CharacterDict, session: Optional[Session] = None) -> Character | None:
        """
        Update an existing character.

        Args:
            character_id: The ID of the character to update.
            data: CharacterDict containing updated character details.

        Returns:
            Updated Character object if successful, else None
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            existing = self.get_by_id(character_id, session=session)

            if not existing:
                logger.warning(f"Character not found: {character_id}")
                return None
            
            update_data = data.model_dump(exclude={'id', 'language_id', 'difficulty', 'status', 'score', 'created_at', 'last_seen_at', 'tags', 'sources'}, exclude_none=True)
            logger.info(f"Update data for character {character_id}: {update_data}")

            if (existing_character := self.get_by_character(update_data['character'], language_id=existing.language_id, session=session)) and existing_character.id != character_id:
                logger.warning(f"Character with value '{update_data['character']}' already exists.")
                raise ValueError(f"Character with value '{update_data['character']}' already exists.")

            language = db_manager.find_by_attr(model_class=Language, attr_values={"id": existing.language_id}, session=session)

            source_iso1 = get_language_by_iso2t(language.source_iso639_2t).iso1 if language else None
            target_iso1 = get_language_by_iso2t(language.target_iso639_2t).iso1 if language else None

            enriched_data = enrich_character(character_text=update_data['character'], target_iso1=target_iso1, source_iso1=source_iso1)

            def resolve(field: str, existing_val):
                provided = update_data.get(field)
                if provided is not None and provided != "":
                    return provided
                return existing_val if existing_val is not None and existing_val != "" else enriched_data.get(field)
            
            logger.debug(update_data)

            existing.character = update_data.get('character', existing.character)
            existing.phonetic = resolve('phonetic', existing.phonetic)
            existing.radical = resolve('radical', existing.radical)
            existing.meaning = resolve('meaning', existing.meaning)
            existing.strokes = update_data.get('strokes', existing.strokes)
            existing.audio_files = update_data.get('audio_files', existing.audio_files)
            existing.image_files = update_data.get('image_files', existing.image_files)

            logger.debug(existing.to_dict(False))
            
            # Save to database
            result = db_manager.modify(existing, session=session)

            logger.debug(result.to_dict(False))

            if result:
                logger.info(f"Updated character: {character_id}")
            else:
                logger.error(f"Failed to update character: {character_id}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update character {character_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, character_id: str, session: Optional[Session] = None) -> bool:
        """
        Delete a character by its ID.

        Args:
            character_id: The ID of the character to delete.

        Returns:
            True if deletion was successful, else False
        """
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()
        
        try:
            # Check if character exists before deleting
            existing = self.get_by_id(character_id, session=session)

            if not existing:
                logger.warning(f"Character not found: {character_id}")
                return False

            # Delete from database
            success = db_manager.delete(existing, session=session)

            if success:
                logger.info(f"Deleted character: {character_id}")
            else:
                logger.error(f"Failed to delete character: {character_id}")

            return success
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete character {character_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update_score(self, char_id: str, session: Optional[Session] = None) -> Character | None:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            character = self.get_by_id(char_id, session=session)
            if not character:
                logger.warning(f"Character not found: {char_id}")
                return None

            # Recalculate score based on all related features
            features = [
                *character.calligraphy
            ]
            
            if features and len(features) > 0:
                total_score = sum(feature.score for feature in features)
                character.score = total_score / len(features)
                
                total_difficulty = sum(feature.difficulty for feature in features)
                character.difficulty = total_difficulty / len(features)
            else:
                logger.warning(f"No features found for character: {char_id}")
                character.score = 0.0
                character.difficulty = 0.5

            character.last_seen_at = datetime.now()

            result = db_manager.modify(character, session=session)

            if result:
                logger.info(f"Updated CharacterComponent {char_id} score to {character.score} and difficulty to {character.difficulty}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update character score for {char_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()