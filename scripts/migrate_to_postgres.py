#!/usr/bin/env python3
"""Copy each config's legacy SQLite database into its Postgres schema.

Idempotent: uses INSERT ... ON CONFLICT DO NOTHING keyed on each table's
primary key, so re-running never duplicates rows. Safe to run repeatedly
while iterating, and safe to re-run after a partial failure.

Usage:
    python scripts/migrate_to_postgres.py [--dry-run] [--config dev|test|prod ...]
"""
import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.types import JSON, Boolean, DateTime, Date, Integer

# Legacy CEFR-style level exports seen in corrupted data; anything else
# unrecognized falls back to 0 (unstarted) rather than guessing further.
CEFR_LEVEL_MAP = {"A1": 0, "A2": 1, "B1": 2, "B2": 3, "C1": 4, "C2": 5}

import lapp.models  # noqa: F401 - registers all tables on Base.metadata
from lapp.core.database import Base
from config import config as app_config

# FK-safe insert order (mirrors docs/migrations/old_to_new.sql's dependency
# chain). language/lesson are mutually dependent (language.current_lesson_id
# -> lesson.id, lesson.language_id -> language.id) - language is inserted
# first with that column nulled out, then patched after lesson is inserted.
TABLE_ORDER = [
    "user", "user_preferences", "source", "tag",
    "language", "lesson",
    "word", "character", "passage",
    "vocabulary", "grammar", "calligraphy", "exercise",
    "progress_tracking", "daily_stats", "commitment_log",
    "word_passage_link", "character_word_link", "character_passage_link",
    "vocabulary_example_sentence", "calligraphy_example_word", "calligraphy_example_sentence",
    "grammar_example_word", "grammar_example_sentence",
    "exercise_vocabulary_link", "exercise_grammar_link", "exercise_calligraphy_link",
    "source_element_link", "tag_element_link",
]

SOURCES = {
    "dev": REPO_ROOT / "instance" / "dev_languages.db",
    "test": REPO_ROOT / "instance" / "test_languages.db",
    "prod": REPO_ROOT / "instance" / "languages.db",
}


def _count_stmt(table):
    return select(func.count()).select_from(table)


def _coerce_int(table_name: str, col_name: str, row_id, value):
    """Best-effort coercion for a legacy export where an Integer column holds
    a CEFR string ("A1") or a float (83.77) instead of an int. Logs every
    coercion so corrupted source rows can be audited afterward.
    """
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value in CEFR_LEVEL_MAP:
        coerced = CEFR_LEVEL_MAP[value]
    else:
        try:
            coerced = int(round(float(value)))
        except (TypeError, ValueError):
            coerced = 0
    print(f"    [coerce] {table_name}.{col_name} id={row_id}: {value!r} -> {coerced}")
    return coerced


def _coerce_row(table, row: dict) -> dict:
    """Adapt one sqlite3.Row (as dict) to the target column types.

    sqlite has no native JSON/bool/datetime types - it stores them as text/int.
    Generated (Computed) columns like `status` can't be inserted into at all.
    """
    out = {}
    for col in table.columns:
        if col.name not in row or col.computed is not None:
            continue
        value = row[col.name]
        if value is None:
            out[col.name] = None
        elif isinstance(col.type, JSON) and isinstance(value, str):
            out[col.name] = json.loads(value)
        elif isinstance(col.type, Boolean):
            out[col.name] = bool(value)
        elif isinstance(col.type, (DateTime, Date)) and isinstance(value, str):
            out[col.name] = datetime.fromisoformat(value)
        elif isinstance(col.type, Integer) and not isinstance(value, int):
            out[col.name] = _coerce_int(table.name, col.name, row.get("id"), value)
        else:
            out[col.name] = value
    return out


def migrate_one(engine, sqlite_path: Path, schema: str, dry_run: bool) -> dict:
    """Copy every table for one config. Returns {table: (source_rows, inserted)}."""
    sconn = sqlite3.connect(str(sqlite_path))
    sconn.row_factory = sqlite3.Row
    existing_tables = {
        r[0] for r in sconn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }

    results = {}
    valid_ids = {}  # table_name -> set of ids successfully migrated, for FK nulling

    with engine.begin() as conn:
        for table_name in TABLE_ORDER:
            if table_name not in existing_tables:
                continue
            table = Base.metadata.tables[table_name]
            rows = [dict(r) for r in sconn.execute(f'SELECT * FROM "{table_name}"')]
            if not rows:
                results[table_name] = (0, 0)
                continue

            coerced = [_coerce_row(table, r) for r in rows]

            # language.current_lesson_id is populated with stale/unmapped ids
            # in some legacy exports; null it out here and patch it below
            # once `lesson` has actually been inserted and we know real ids.
            if table_name == "language":
                for r in coerced:
                    r["current_lesson_id"] = None

            pk_cols = [c.name for c in table.primary_key.columns]
            stmt = pg_insert(table).values(coerced)
            stmt = stmt.on_conflict_do_nothing(index_elements=pk_cols)

            if dry_run:
                results[table_name] = (len(rows), 0)
                valid_ids[table_name] = {r[pk_cols[0]] for r in coerced} if len(pk_cols) == 1 else set()
                continue

            # psycopg doesn't report a usable rowcount for multi-row VALUES
            # inserts; count before/after instead.
            before = conn.execute(_count_stmt(table)).scalar()
            conn.execute(stmt)
            after = conn.execute(_count_stmt(table)).scalar()
            results[table_name] = (len(rows), after - before)
            if len(pk_cols) == 1:
                valid_ids[table_name] = {r[pk_cols[0]] for r in coerced}

        # Second pass: patch language.current_lesson_id now that lesson rows
        # exist, only where the source value actually refers to a migrated lesson.
        if not dry_run and "language" in existing_tables and "lesson" in valid_ids:
            for r in sconn.execute('SELECT id, current_lesson_id FROM "language"'):
                lesson_id = r["current_lesson_id"]
                if lesson_id and lesson_id in valid_ids.get("lesson", set()):
                    conn.execute(
                        Base.metadata.tables["language"]
                        .update()
                        .where(Base.metadata.tables["language"].c.id == r["id"])
                        .values(current_lesson_id=lesson_id)
                    )

    sconn.close()
    return results


def validate_counts(engine, sqlite_path: Path) -> None:
    sconn = sqlite3.connect(str(sqlite_path))
    existing_tables = {
        r[0] for r in sconn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    with engine.connect() as conn:
        for table_name in TABLE_ORDER:
            if table_name not in existing_tables:
                continue
            source_count = sconn.execute(f'SELECT COUNT(*) FROM "{table_name}"').fetchone()[0]
            pg_count = conn.execute(_count_stmt(Base.metadata.tables[table_name])).scalar()
            status = "OK" if pg_count >= source_count else "MISMATCH"
            print(f"    {table_name}: source={source_count} postgres={pg_count} [{status}]")
    sconn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--config", nargs="+", choices=["dev", "test", "prod"], default=["dev", "test", "prod"])
    args = parser.parse_args()

    from sqlalchemy import create_engine

    for env_name in args.config:
        sqlite_path = SOURCES[env_name]
        if not sqlite_path.exists():
            print(f"[{env_name}] no SQLite file at {sqlite_path}, skipping")
            continue

        cfg = app_config[env_name]
        print(f"[{env_name}] migrating {sqlite_path} -> schema {cfg.DB_SCHEMA} ({'dry-run' if args.dry_run else 'live'})")
        engine = create_engine(cfg.SQLALCHEMY_DATABASE_URI)
        results = migrate_one(engine, sqlite_path, cfg.DB_SCHEMA, args.dry_run)
        for table_name, (source_rows, inserted) in results.items():
            if source_rows:
                print(f"    {table_name}: {source_rows} in source, {inserted} inserted")

        if not args.dry_run:
            print(f"[{env_name}] validating row counts")
            validate_counts(engine, sqlite_path)
        engine.dispose()


if __name__ == "__main__":
    main()
