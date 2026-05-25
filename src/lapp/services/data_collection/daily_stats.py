from datetime import datetime, timedelta
from typing import Optional

import logging
from sqlalchemy import func
from sqlalchemy.orm import Session

from ...core.database import db_manager
from ...models.data_collection.daily_stats import DailyStats
from ...models.data_collection.progress_tracking import ProgressTracking

logger = logging.getLogger(__name__)


class DailyStatsService:
    def _serialize(
        self,
        entry: DailyStats | None,
        as_dict: bool,
        include_relations: bool,
    ) -> DailyStats | dict | None:
        if not as_dict or entry is None:
            return entry
        return entry.to_dict(include_relations=include_relations)

    def _serialize_list(
        self,
        entries: list[DailyStats],
        as_dict: bool,
        include_relations: bool,
    ) -> list[DailyStats] | list[dict]:
        if not as_dict:
            return entries
        return [entry.to_dict(include_relations=include_relations) for entry in entries]

    def get_by_id(
        self,
        daily_stats_id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True,
    ) -> DailyStats | dict | None:
        """Get a DailyStats entry by its ID."""
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            entry = db_manager.find_by_attr(
                model_class=DailyStats,
                attr_values={"id": daily_stats_id},
                session=session,
            )
            return self._serialize(entry, as_dict, include_relations)
        except Exception as error:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get daily stats entry by id: {error}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_today_for_user(
        self,
        user_id: str,
        language_id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True,
    ) -> DailyStats | dict | None:
        """Get today's DailyStats entry for a specific user and language, creating it if needed."""
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            today = datetime.utcnow().date()
            entry = (
                session.query(DailyStats)
                .filter(
                    DailyStats.user_id == user_id,
                    DailyStats.language_id == language_id,
                    func.date(DailyStats.created_at) == today.isoformat(),
                )
                .first()
            )

            if entry is None:
                entry = self.create(user_id=user_id, language_id=language_id, session=session)

            return self._serialize(entry, as_dict, include_relations)
        except Exception as error:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get today's daily stats entry: {error}")
            raise
        finally:
            if owns_session:
                session.close()

    def get_today_for_user_no_create(
        self,
        user_id: str,
        language_id: str,
        session: Optional[Session] = None,
        as_dict: bool = False,
        include_relations: bool = True,
    ) -> DailyStats | dict | None:
        """Get today's DailyStats entry without creating a new row."""
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            today = datetime.now().date()
            entry = (
                session.query(DailyStats)
                .filter(
                    DailyStats.user_id == user_id,
                    DailyStats.language_id == language_id,
                    func.date(DailyStats.created_at) == today.isoformat(),
                )
                .first()
            )
            return self._serialize(entry, as_dict, include_relations)
        except Exception as error:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to get today's daily stats entry without creating one: {error}")
            raise
        finally:
            if owns_session:
                session.close()

    def create(
        self,
        user_id: str,
        language_id: str,
        session: Session,
    ) -> DailyStats:
        """
        Insert a new row into daily_stats.

        When called from another service, the caller passes its own open
        session so the insert shares one transaction.
        """
        entry = DailyStats(
            id=db_manager.generate_new_id(model_class=DailyStats, session=session),
            user_id=user_id,
            language_id=language_id,
            items_reviewed=0,
            items_correct=0,
            time_studied_ms=0,
            streak_day=False,
            current_streak_length=0,
        )
        result = db_manager.insert(obj=entry, session=session)
        if result is None:
            raise RuntimeError("Failed to create daily stats entry")
        return result

    def update(
        self,
        progress_tracking_id: str,
        session: Session,
    ) -> DailyStats:
        """
        Apply a progress tracking entry to today's daily stats row.

        This method expects an open session owned by the caller.
        """
        progress_tracking = db_manager.find_by_attr(
            model_class=ProgressTracking,
            attr_values={"id": progress_tracking_id},
            session=session,
        )

        if progress_tracking is None:
            raise ValueError(f"ProgressTracking entry not found: {progress_tracking_id}")

        daily_stats = self.get_today_for_user(
            user_id=progress_tracking.user_id,
            language_id=progress_tracking.language_id,
            session=session,
        )

        if daily_stats is None:
            raise RuntimeError("Failed to load or create today's daily stats entry")

        daily_stats.items_reviewed += 1
        if progress_tracking.result is True:
            daily_stats.items_correct += 1
        daily_stats.time_studied_ms += int(progress_tracking.duration_ms)

        if daily_stats.items_reviewed >= 20 and daily_stats.streak_day is False:
            daily_stats.streak_day = True

            yesterday = (datetime.utcnow() - timedelta(days=1)).date().isoformat()
            previous_daily_stats = (
                session.query(DailyStats)
                .filter(
                    DailyStats.user_id == progress_tracking.user_id,
                    DailyStats.language_id == progress_tracking.language_id,
                    DailyStats.streak_day.is_(True),
                    func.date(DailyStats.created_at) == yesterday,
                )
                .order_by(DailyStats.created_at.desc())
                .first()
            )

            if previous_daily_stats is not None:
                daily_stats.current_streak_length = previous_daily_stats.current_streak_length + 1
            else:
                daily_stats.current_streak_length = 1

        result = db_manager.modify(obj=daily_stats, session=session)
        if result is None:
            raise RuntimeError(f"Failed to update daily stats entry for progress tracking {progress_tracking_id}")
        return result