from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

import logging

from ...core.database import db_manager
from ...models.features import Exercise
from ...schemas.features import ExerciseDict
from ...utils import update_score, update_difficulty
from ..containers import LessonService
from .calligraphy import CalligraphyService
from .grammar import GrammarService
from .vocabulary import VocabularyService

logger = logging.getLogger(__name__)

lesson_service = LessonService()
calligraphy_service = CalligraphyService()
grammar_service = GrammarService()
vocabulary_service = VocabularyService()

class ExerciseService:
    def _serialize(self, exercise: Exercise | None, as_dict: bool, include_relations: bool) -> Exercise | dict | None:
        if not as_dict or exercise is None:
            return exercise
        return exercise.to_dict(include_relations=include_relations)

    def _serialize_list(self, exercises: list[Exercise], as_dict: bool, include_relations: bool) -> list[Exercise] | list[dict]:
        if not as_dict:
            return exercises
        return [exercise.to_dict(include_relations=include_relations) for exercise in exercises]

    def _resolve_associations(
        self,
        calligraphy_ids: Optional[list[str]],
        vocabulary_ids: Optional[list[str]],
        grammar_ids: Optional[list[str]],
        session: Optional[Session],
    ) -> tuple[list, list, list]:
        calligraphies = [
            c
            for cid in (calligraphy_ids or [])
            if (c := calligraphy_service.get_by_id(calligraphy_id=cid, session=session))
        ]
        vocabularies = [
            v
            for vid in (vocabulary_ids or [])
            if (v := vocabulary_service.get_by_id(voc_id=vid, session=session))
        ]
        grammars = [
            g
            for gid in (grammar_ids or [])
            if (g := grammar_service.get_by_id(grammar_id=gid, session=session))
        ]
        return calligraphies, vocabularies, grammars

    def get_all(
        self,
        language_id: Optional[str] = None,
        lesson_id: Optional[str] = None,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True,
    ) -> list[Exercise] | list[dict]:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            assert not (language_id and lesson_id), f"language_id and lesson_id can't both be specified: {language_id}, {lesson_id}"
            if language_id:
                lessons = lesson_service.get_all(language_id=language_id, session=session)
                exercises: list[Exercise] = []
                for lesson in lessons:
                    exercises.extend(
                        db_manager.find_all(
                            model_class=Exercise,
                            filters={"lesson_id": lesson.id},
                            session=session,
                        )
                    )
            elif lesson_id:
                exercises = db_manager.find_all(
                    model_class=Exercise,
                    filters={"lesson_id": lesson_id},
                    session=session,
                )
            else:
                raise ValueError(f"Requires either language_id or lesson_id but got: {language_id}, {lesson_id}")

            return self._serialize_list(exercises, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get exercises: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_by_id(
        self,
        ex_id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True,
    ) -> Exercise | dict | None:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            exercise = db_manager.find_by_attr(
                model_class=Exercise,
                attr_values={"id": ex_id},
                session=session,
            )
            return self._serialize(exercise, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get exercise by id: {e}")
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
        include_relations: bool = True,
    ) -> list[Exercise] | list[dict]:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            assert not (language_id and lesson_id), f"language_id and lesson_id can't both be specified: {language_id}, {lesson_id}"

            if language_id:
                lessons = lesson_service.get_all(language_id=language_id, session=session)
                exercises: list[Exercise] = []
                for lesson in lessons:
                    exercises.extend(
                        db_manager.find_all(
                            model_class=Exercise,
                            filters={"lesson_id": lesson.id, "level": level},
                            session=session,
                        )
                    )
            elif lesson_id:
                exercises = db_manager.find_all(
                    model_class=Exercise,
                    filters={"lesson_id": lesson_id, "level": level},
                    session=session,
                )
            else:
                raise ValueError(f"Requires either language_id or lesson_id but got: {language_id}, {lesson_id}")

            return self._serialize_list(exercises, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get exercises by level: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def create(
        self,
        data: ExerciseDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True,
    ) -> Exercise | dict | None:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            lesson = lesson_service.get_by_id(data.lesson_id, session=session)
            if not lesson:
                logger.warning(f"Cannot create exercise, lesson not found: {data.lesson_id}")
                return None

            exercise_data = data.model_dump(exclude_none=True)
            exercise_data.pop("last_seen_at", None)
            calligraphy_ids = exercise_data.pop("calligraphy_ids", None)
            vocabulary_ids = exercise_data.pop("vocabulary_ids", None)
            grammar_ids = exercise_data.pop("grammar_ids", None)

            exercise = Exercise(
                id=db_manager.generate_new_id(model_class=Exercise, session=session),
                **exercise_data,
            )
            exercise.calligraphy, exercise.vocabulary, exercise.grammar = self._resolve_associations(
                calligraphy_ids=calligraphy_ids,
                vocabulary_ids=vocabulary_ids,
                grammar_ids=grammar_ids,
                session=session,
            )

            result = db_manager.insert(obj=exercise, session=session)
            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to create exercise: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update(
        self,
        ex_id: str,
        data: ExerciseDict,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True,
    ) -> Exercise | dict | None:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            existing = self.get_by_id(ex_id, session=session)
            if not existing:
                logger.warning(f"Exercise not found: {ex_id}")
                return None

            update_data = data.model_dump(exclude_none=True)
            update_data.pop('id', None)  # Don't allow updating the ID
            update_data.pop('score', None)  # Don't allow direct score updates
            update_data.pop('difficulty', None)  # Don't allow direct difficulty updates
            update_data.pop('status', None)  # Don't allow direct status updates
            update_data.pop('created_at', None)  # Don't allow updating created_at
            update_data.pop('last_seen_at', None)   # Don't allow direct last_seen_at updates

            if "lesson_id" in update_data and not lesson_service.get_by_id(update_data["lesson_id"], session=session):
                update_data["lesson_id"] = existing.lesson_id

            calligraphy_ids = update_data.pop("calligraphy_ids", None)
            vocabulary_ids = update_data.pop("vocabulary_ids", None)
            grammar_ids = update_data.pop("grammar_ids", None)

            for key, value in update_data.items():
                setattr(existing, key, value)

            if calligraphy_ids is not None or vocabulary_ids is not None or grammar_ids is not None:
                existing.calligraphy, existing.vocabulary, existing.grammar = self._resolve_associations(
                    calligraphy_ids=calligraphy_ids,
                    vocabulary_ids=vocabulary_ids,
                    grammar_ids=grammar_ids,
                    session=session,
                )

            result = db_manager.modify(existing, session=session)
            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update exercise: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def delete(self, ex_id: str, session: Optional[Session] = None) -> bool:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            existing = self.get_by_id(ex_id, session=session)
            if not existing:
                return False
            return db_manager.delete(existing, session=session)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to delete exercise: {e}")
            raise
        finally:
            if owns_session:
                session.close()

    def update_score(
        self,
        ex_id: str,
        score: float,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True,
    ) -> Exercise | dict | None:
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            exercise = self.get_by_id(ex_id, session=session)
            if not exercise:
                logger.warning(f"Exercise not found: {ex_id}")
                return None

            previous_score = exercise.score
            exercise.score = update_score(
                score=exercise.score,
                last_seen_at=exercise.last_seen_at,
                similarity=score,
            )
            exercise.difficulty = update_difficulty(
                new_score=exercise.score,
                last_seen_at=exercise.last_seen_at,
                previous_difficulty=exercise.difficulty,
                created_at=exercise.created_at
            )

            exercise.last_seen_at = datetime.now()    

            result = db_manager.modify(exercise, session=session)

            if result:
                logger.info(f"Updated exercise {ex_id} score to {exercise.score} and difficulty to {exercise.difficulty}")

            for vocabulary in exercise.vocabulary:
                vocabulary_service.update_score(vocabulary.id, score=score, session=session)
                logger.info(f"Updated vocabulary {vocabulary.id} score due to exercise {ex_id}")

            for grammar in exercise.grammar:
                grammar_service.update_score(grammar.id, score=score, session=session)
                logger.info(f"Updated grammar {grammar.id} score due to exercise {ex_id}")

            for calligraphy in exercise.calligraphy:
                calligraphy_service.update_score(calligraphy.id, score=score, session=session)
                logger.info(f"Updated calligraphy {calligraphy.id} score due to exercise {ex_id}")

            if exercise.score != previous_score:
                lesson_service.update_score(exercise.lesson_id, session=session)
                logger.info(f"Updated lesson {exercise.lesson_id} score due to exercise {ex_id}")

            return self._serialize(result, as_dict, include_relations)
        except Exception as e:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to update exercise score for {ex_id}: {e}")
            raise
        finally:
            if owns_session:
                session.close()
