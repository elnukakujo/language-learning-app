"""Phase 5c: duplicate-resolution for Word/Character creation.

Locks in the contract: creating a Word/Character that already exists for the
language raises DuplicateEntityError by default (was: silent upsert), and
"keep" / "overwrite" / "merge" resolve it explicitly. Internal derivation
(auto-creating characters found within a word, words/characters tokenized
out of a passage, calligraphy/grammar example words) must keep the old
silent-merge behavior — those aren't the user's top-level create action.
"""
import pytest

from lapp.core.exceptions import DuplicateEntityError
from lapp.core.database import db_manager
from lapp.models.system_data import User
from lapp.models.containers import Language
from lapp.services.components.word import WordService
from lapp.services.components.character import CharacterService
from lapp.schemas.components import WordDict, CharacterDict

word_service = WordService()
character_service = CharacterService()


def _seed_language(db, target="fra", source="eng"):
    with db.session_scope() as s:
        db.insert(User(id="user_D1", username="dup_tester"), session=s, commit=False)
        db.insert(Language(id="lang_D1", user_id="user_D1", name="French",
                           target_iso639_2t=target, source_iso639_2t=source),
                  session=s, commit=False)


def test_word_create_raises_on_conflict_by_default(db):
    _seed_language(db)
    first = word_service.create(WordDict(word="bonjour", language_id="lang_D1", translation="hello"))
    assert first is not None

    with pytest.raises(DuplicateEntityError) as exc_info:
        word_service.create(WordDict(word="bonjour", language_id="lang_D1", translation="hi there"))

    err = exc_info.value
    assert err.entity_type == "word"
    assert err.existing["id"] == first.id
    assert "translation" in err.diff  # existing="hello" vs incoming="hi there"


def test_word_create_keep_returns_existing_unchanged(db):
    _seed_language(db)
    first = word_service.create(WordDict(word="bonjour", language_id="lang_D1", translation="hello"))

    kept = word_service.create(
        WordDict(word="bonjour", language_id="lang_D1", translation="hi there"),
        on_conflict="keep",
    )

    assert kept.id == first.id
    assert kept.translation == "hello"  # untouched


def test_word_create_overwrite_ignores_existing_value(db):
    """Overwrite never consults the existing row: incoming wins, blanks fall
    back to fresh enrichment — not to whatever was there before. (Schemas
    normalize "" to None before this runs, so "explicitly blanked" and
    "omitted" are indistinguishable — recomputing via enrichment for an
    omitted field is the correct, well-defined behavior, not a shortcut.)"""
    _seed_language(db)
    first = word_service.create(WordDict(word="bonjour", language_id="lang_D1", translation="hello", word_type="verb"))

    overwritten = word_service.create(
        WordDict(word="bonjour", language_id="lang_D1", translation="hi there"),
        on_conflict="overwrite",
    )

    assert overwritten.id == first.id
    assert overwritten.translation == "hi there"
    assert overwritten.word_type != "verb"  # existing value never consulted under overwrite


def test_word_create_merge_fills_blanks_from_existing(db):
    _seed_language(db)
    first = word_service.create(WordDict(word="bonjour", language_id="lang_D1", translation="hello", word_type="interjection"))

    merged = word_service.create(
        WordDict(word="bonjour", language_id="lang_D1", translation="hi there", word_type=""),
        on_conflict="merge",
    )

    assert merged.id == first.id
    assert merged.translation == "hi there"       # incoming non-blank wins
    assert merged.word_type == "interjection"      # incoming blank falls back to existing


def test_character_create_raises_on_conflict_by_default(db):
    _seed_language(db, target="zho", source="eng")
    first = character_service.create(CharacterDict(character="学", language_id="lang_D1", phonetic="xué"))

    with pytest.raises(DuplicateEntityError) as exc_info:
        character_service.create(CharacterDict(character="学", language_id="lang_D1", phonetic="xue2"))

    assert exc_info.value.entity_type == "character"
    assert exc_info.value.existing["id"] == first.id


def test_word_create_still_auto_derives_characters_without_conflict(db):
    """Internal character derivation must not raise even though '学' recurs."""
    _seed_language(db, target="zho", source="eng")

    word1 = word_service.create(WordDict(word="学生", language_id="lang_D1"))
    assert word1 is not None
    # A second, different word sharing a character with the first must not raise,
    # even though on_conflict was never specified for this top-level create() call.
    word2 = word_service.create(WordDict(word="学校", language_id="lang_D1"))
    assert word2 is not None


if __name__ == "__main__":
    print("run via: uv run pytest tests/test_duplicate_resolution.py")
