from datetime import datetime, timedelta
from typing import Optional

import logging
logger = logging.getLogger(__name__)
from sqlalchemy import func
from sqlalchemy.orm import Session

from ...core.database import db_manager
from ...models.data_collection.daily_stats import DailyStats
from ...models.data_collection.progress_tracking import ProgressTracking
from ..system_data import UserPreferencesService
user_preferences_service = UserPreferencesService()
from .commitment_log import CommitmentLogService
commitment_log_service = CommitmentLogService()

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

    def is_session_complete(
        self,
        user_id: str,
        language_id: str,
        session: Optional[Session] = None
    ) -> bool:
        """Check if the current session has any progress tracking entries that haven't been applied to daily stats."""
        owns_session = session is None
        if owns_session:
            session = db_manager.get_session()

        try:
            today: datetime.date = datetime.now().date()
            language_stats = db_manager.find_by_attr(
                model_class=DailyStats,
                attr_values={"user_id": user_id, "language_id": language_id},
                session=session,
                many=True
            )

            for stats in list(language_stats):
                if stats.created_at.date() == today:
                    today_stats = stats
                    break
            return today_stats.streak_day is True if today_stats else False
        except Exception as error:
            if owns_session:
                session.rollback()
            logger.error(f"Failed to check if session is complete: {error}")
            raise
        finally:
            if owns_session:
                session.close()

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

        daily_stats: DailyStats = self.get_today_for_user(
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

        user_preferences = user_preferences_service.get_by_user_id(user_id=progress_tracking.user_id, session=session)
        if user_preferences is None:
            logger.warning(f"User preferences not found for user {progress_tracking.user_id}. Skipping streak day check.")
            daily_goal_ms = 20 * 60 * 1000  # Default to 20 minutes if user preferences are missing
        else:
            daily_goal_ms = user_preferences.daily_goal_minutes * 60 * 1000

        streak_just_set = False
        if daily_stats.time_studied_ms >= daily_goal_ms and daily_stats.streak_day is False:
            streak_just_set = True
            daily_stats.streak_day = True
            logger.info(f"User {progress_tracking.user_id} just achieved a streak day for language {progress_tracking.language_id}!")

            yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
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

        # If we just set today's streak flag, propagate to the commitment log
        if daily_stats.streak_day is True and streak_just_set:
            commitment_log_service.apply_daily_stats(
                daily_stats_id=daily_stats.id,
                session=session,
            )

        return result