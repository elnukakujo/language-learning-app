import logging
from typing import Optional
import datetime
from sqlalchemy.orm import Session

from ...core.database import db_manager
from ...models.components import Word
from ...models.features import Vocabulary, Calligraphy, Grammar
from ...schemas.components import WordDict

logger = logging.getLogger(__name__)

class WordService:
    def get_all(self, session: Optional[Session] = None) -> list[Word]:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            return db_manager.find_all(model_class=Word, session=session)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get all words: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(self, word_id: str, session: Optional[Session] = None) -> Word | None:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            return db_manager.find_by_attr(
                model_class=Word,
                attr_values={"id": word_id},
                session=session,
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get word {word_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_word(
        self,
        word: str,
        language_id: Optional[str] = None,
        session: Optional[Session] = None,
    ) -> Word | None:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            filters = {"word": word}
            if language_id:
                filters["language_id"] = language_id
            return db_manager.find_by_attr(
                model_class=Word,
                attr_values=filters,
                session=session,
            )
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get word by value '{word}': {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def create(self, data: WordDict, session: Optional[Session] = None) -> Word | None:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            if existing := self.get_by_word(data.word, language_id=data.language_id, session=session):
                logger.info(f"Word already exists: {data.word} with ID: {existing.id}")
                return self.update(word_id=existing.id, data=data, session=session)

            word_data = data.model_dump(exclude_none=True)
            word_data.pop("last_seen_at", None)
            if "type" in word_data:
                word_data["word_type"] = word_data.pop("type")
            if "gender" in word_data:
                word_data["word_gender"] = word_data.pop("gender")

            word = Word(
                id=db_manager.generate_new_id(model_class=Word, session=session),
                **word_data,
            )
            result = db_manager.insert(obj=word, session=session)
            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create word: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(self, word_id: str, data: WordDict, session: Optional[Session] = None) -> Word | None:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            existing = self.get_by_id(word_id, session=session)
            if not existing:
                logger.warning(f"Word not found: {word_id}")
                return None

            update_data = data.model_dump(exclude_none=True)
            update_data.pop("id", None)
            update_data.pop("score", None)
            update_data.pop("last_seen", None)
            update_data.pop("last_seen_at", None)
            if "type" in update_data:
                update_data["word_type"] = update_data.pop("type")
            if "gender" in update_data:
                update_data["word_gender"] = update_data.pop("gender")

            incoming_word = update_data.get("word")
            if incoming_word:
                conflict = self.get_by_word(incoming_word, language_id=existing.language_id, session=session)
                if conflict and conflict.id != word_id:
                    raise ValueError(f"Word with value '{incoming_word}' already exists.")

            for key, value in update_data.items():
                setattr(existing, key, value)

            return db_manager.modify(existing, session=session)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update word {word_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, word_id: str, session: Optional[Session] = None) -> bool:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            existing = self.get_by_id(word_id, session=session)
            if not existing:
                logger.warning(f"Word not found: {word_id}")
                return False
            return db_manager.delete(existing, session=session)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete word {word_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
    def update_score(self, word_id: str, session: Optional[Session] = None) -> Word | None:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            word = self.get_by_id(word_id, session=session)
            if not word:
                logger.warning(f"Word not found: {word_id}")
                return None

            # Recalculate score based on all related features
            features = []
            for voc_id in word.vocabulary_ids:
                voc = db_manager.find_by_id(Vocabulary, voc_id, session=session)
                if voc:
                    features.append(voc)
            for gram_id in word.grammar_ids:
                gram = db_manager.find_by_id(Grammar, gram_id, session=session)
                if gram:
                    features.append(gram)
            for call_id in word.calligraphy_ids:
                call = db_manager.find_by_id(Calligraphy, call_id, session=session)
                if call:
                    features.append(call)
            
            if features and len(features) > 0:
                total_score = sum(feature.score for feature in features)
                word.score = total_score / len(features)

                total_difficulty = sum(feature.difficulty for feature in features)
                word.difficulty = total_difficulty / len(features)
            else:
                logger.warning(f"No features found for word: {word_id}")
                word.score = 0.0
                word.difficulty = 0.5
                
            # Update last_seen
            word.last_seen = datetime.now()

            result = db_manager.modify(word, session=session)

            if result:
                logger.info(f"Updated WordComponent {word_id} score to {word.score} and difficulty to {word.difficulty}")

            return result
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update word score for {word_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()