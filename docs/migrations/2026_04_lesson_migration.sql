PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

-- ============================================================================
-- 0) Pre-flight check
-- ============================================================================

SELECT 'Pre-migration row counts:' AS info;
SELECT 'language' AS tbl, COUNT(*) AS rows FROM language
UNION ALL SELECT 'unit',        COUNT(*) FROM unit
UNION ALL SELECT 'word',        COUNT(*) FROM word
UNION ALL SELECT 'character',   COUNT(*) FROM character
UNION ALL SELECT 'passage',     COUNT(*) FROM passage
UNION ALL SELECT 'vocabulary',  COUNT(*) FROM vocabulary
UNION ALL SELECT 'grammar',     COUNT(*) FROM grammar
UNION ALL SELECT 'calligraphy', COUNT(*) FROM calligraphy
UNION ALL SELECT 'exercise',    COUNT(*) FROM exercise;

-- ============================================================================
-- 1) Preserve current tables
-- ============================================================================

ALTER TABLE language    RENAME TO old_language;
ALTER TABLE unit        RENAME TO old_unit;
ALTER TABLE word        RENAME TO old_word;
ALTER TABLE character   RENAME TO old_character;
ALTER TABLE passage     RENAME TO old_passage;
ALTER TABLE vocabulary  RENAME TO old_vocabulary;
ALTER TABLE grammar     RENAME TO old_grammar;
ALTER TABLE calligraphy RENAME TO old_calligraphy;
ALTER TABLE exercise    RENAME TO old_exercise;

-- ============================================================================
-- 2) Create new schema
-- ============================================================================

-- ---- System data ----

CREATE TABLE user (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    day_streak INTEGER NOT NULL DEFAULT 0,
    last_review DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_preferences (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    native_language_iso639_2 JSON NOT NULL DEFAULT '["eng"]',
    learning_goals TEXT DEFAULT '',
    preferred_exercise_types JSON DEFAULT '[]',
    last_updated DATE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE source (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    date DATE,
    description TEXT,
    source_type TEXT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE tag (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    tagged_element_type TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT,
    description TEXT,
    UNIQUE (user_id, name),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- ---- Containers ----
-- NOTE: language must be created before strengths_and_weaknesses and
--       progress_tracking so their FKs resolve correctly.

CREATE TABLE language (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    -- common container fields
    description TEXT,
    level TEXT NOT NULL DEFAULT 'A1',
    score INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at DATETIME,
    -- language-specific
    name TEXT NOT NULL,
    native_name TEXT,
    flag TEXT,
    target_iso639_2t TEXT,
    source_iso639_2t TEXT DEFAULT 'eng',
    status TEXT NOT NULL GENERATED ALWAYS AS (CASE
        WHEN score = 0  THEN 'unstarted'
        WHEN score <= 30 THEN 'beginner'
        WHEN score <= 60 THEN 'intermediary'
        WHEN score <= 90 THEN 'advanced'
        ELSE 'fluent'
    END) VIRTUAL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    UNIQUE (user_id, name)
);

-- FIX: moved after language so FK to language(id) resolves
CREATE TABLE strengths_and_weaknesses (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    language_id TEXT NOT NULL,
    language_name TEXT NOT NULL,
    element_type TEXT NOT NULL,
    strengths TEXT DEFAULT '',
    weaknesses TEXT DEFAULT '',
    last_updated DATE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (language_id) REFERENCES language(id)
);

-- FIX: moved after language so FK to language(id) resolves
CREATE TABLE progress_tracking (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    language_id TEXT NOT NULL,
    language_name TEXT NOT NULL,
    element_type TEXT NOT NULL,
    element_status TEXT NOT NULL,
    new_score_difference INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    n_reviewed INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (language_id) REFERENCES language(id)
);

CREATE TABLE lesson (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    -- common container fields
    description TEXT,
    level TEXT NOT NULL DEFAULT 'A1',
    score INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at DATETIME,
    -- lesson-specific
    title TEXT,
    status TEXT NOT NULL GENERATED ALWAYS AS (CASE
        WHEN score = 0  THEN 'unstarted'
        WHEN score < 75 THEN 'inprogress'
        WHEN score < 100 THEN 'revisiting'
        ELSE 'completed'
    END) VIRTUAL,
    -- relations
    language_id TEXT NOT NULL,
    FOREIGN KEY (language_id) REFERENCES language(id)
);

-- ---- Components ----

CREATE TABLE word (
    id TEXT PRIMARY KEY,
    -- common component fields
    image_files JSON NOT NULL DEFAULT '[]',
    audio_files JSON NOT NULL DEFAULT '[]',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at DATETIME,
    status TEXT NOT NULL GENERATED ALWAYS AS (CASE
        WHEN score = 0  THEN 'unseen'
        WHEN score <= 10 THEN 'introduced'
        WHEN score <= 50 THEN 'learning'
        WHEN score <= 75 THEN 'practicing'
        WHEN score <= 90 THEN 'review'
        ELSE 'mastered'
    END) VIRTUAL,
    score INTEGER NOT NULL DEFAULT 0,
    difficulty INTEGER NOT NULL DEFAULT 0.5,
    -- word-specific
    word TEXT NOT NULL,
    translation TEXT,
    phonetic TEXT,
    word_type TEXT,
    word_gender TEXT,
    -- relations
    language_id TEXT NOT NULL,
    FOREIGN KEY (language_id) REFERENCES language(id),
    UNIQUE (language_id, word)
);

CREATE TABLE character (
    id TEXT PRIMARY KEY,
    -- common component fields
    image_files JSON NOT NULL DEFAULT '[]',
    audio_files JSON NOT NULL DEFAULT '[]',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at DATETIME,
    status TEXT NOT NULL GENERATED ALWAYS AS (CASE
        WHEN score = 0  THEN 'unseen'
        WHEN score <= 10 THEN 'introduced'
        WHEN score <= 50 THEN 'learning'
        WHEN score <= 75 THEN 'practicing'
        WHEN score <= 90 THEN 'review'
        ELSE 'mastered'
    END) VIRTUAL,
    score INTEGER NOT NULL DEFAULT 0,
    difficulty INTEGER NOT NULL DEFAULT 0.5,
    -- character-specific
    character TEXT NOT NULL,
    phonetic TEXT,
    meaning TEXT,
    radical TEXT,
    strokes INTEGER,
    -- relations
    language_id TEXT NOT NULL,
    FOREIGN KEY (language_id) REFERENCES language(id),
    UNIQUE (language_id, character)
);

CREATE TABLE passage (
    id TEXT PRIMARY KEY,
    -- common component fields
    image_files JSON NOT NULL DEFAULT '[]',
    audio_files JSON NOT NULL DEFAULT '[]',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at DATETIME,
    status TEXT NOT NULL GENERATED ALWAYS AS (CASE
        WHEN score = 0  THEN 'unseen'
        WHEN score <= 10 THEN 'introduced'
        WHEN score <= 50 THEN 'learning'
        WHEN score <= 75 THEN 'practicing'
        WHEN score <= 90 THEN 'review'
        ELSE 'mastered'
    END) VIRTUAL,
    score INTEGER NOT NULL DEFAULT 0,
    difficulty INTEGER NOT NULL DEFAULT 0.5,
    -- passage-specific
    text TEXT NOT NULL,
    translation TEXT,
    -- relations
    language_id TEXT NOT NULL,
    FOREIGN KEY (language_id) REFERENCES language(id),
    UNIQUE (language_id, text)
);

-- ---- Features ----

CREATE TABLE vocabulary (
    id TEXT PRIMARY KEY,
    -- common feature fields
    image_files JSON NOT NULL DEFAULT '[]',
    audio_files JSON NOT NULL DEFAULT '[]',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at DATETIME,
    status TEXT NOT NULL GENERATED ALWAYS AS (CASE
        WHEN score = 0  THEN 'unstarted'
        WHEN score < 75 THEN 'inprogress'
        WHEN score < 100 THEN 'revisiting'
        ELSE 'completed'
    END) VIRTUAL,
    score INTEGER NOT NULL DEFAULT 0,
    difficulty INTEGER NOT NULL DEFAULT 0.5,
    -- relations
    lesson_id TEXT NOT NULL,
    word_id TEXT NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lesson(id),
    FOREIGN KEY (word_id) REFERENCES word(id)
);

CREATE TABLE grammar (
    id TEXT PRIMARY KEY,
    -- common feature fields
    image_files JSON NOT NULL DEFAULT '[]',
    audio_files JSON NOT NULL DEFAULT '[]',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at DATETIME,
    status TEXT NOT NULL GENERATED ALWAYS AS (CASE
        WHEN score = 0  THEN 'unstarted'
        WHEN score < 75 THEN 'inprogress'
        WHEN score < 100 THEN 'revisiting'
        ELSE 'completed'
    END) VIRTUAL,
    score INTEGER NOT NULL DEFAULT 0,
    difficulty INTEGER NOT NULL DEFAULT 0.5,
    -- grammar-specific
    title TEXT,
    explanation TEXT,
    -- relations
    lesson_id TEXT NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lesson(id)
);

CREATE TABLE calligraphy (
    id TEXT PRIMARY KEY,
    -- common feature fields
    image_files JSON NOT NULL DEFAULT '[]',
    audio_files JSON NOT NULL DEFAULT '[]',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at DATETIME,
    status TEXT NOT NULL GENERATED ALWAYS AS (CASE
        WHEN score = 0  THEN 'unstarted'
        WHEN score < 75 THEN 'inprogress'
        WHEN score < 100 THEN 'revisiting'
        ELSE 'completed'
    END) VIRTUAL,
    score INTEGER NOT NULL DEFAULT 0,
    difficulty INTEGER NOT NULL DEFAULT 0.5,
    -- relations
    lesson_id TEXT NOT NULL,
    character_id TEXT NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lesson(id),
    FOREIGN KEY (character_id) REFERENCES character(id)
);

CREATE TABLE exercise (
    id TEXT PRIMARY KEY,
    -- common feature fields
    image_files JSON NOT NULL DEFAULT '[]',
    audio_files JSON NOT NULL DEFAULT '[]',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at DATETIME,
    status TEXT NOT NULL GENERATED ALWAYS AS (CASE
        WHEN score = 0  THEN 'unstarted'
        WHEN score < 75 THEN 'inprogress'
        WHEN score < 100 THEN 'revisiting'
        ELSE 'completed'
    END) VIRTUAL,
    score INTEGER NOT NULL DEFAULT 0,
    difficulty INTEGER NOT NULL DEFAULT 0.5,
    -- exercise-specific
    exercise_type TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    text_support TEXT DEFAULT '',
    -- relations
    lesson_id TEXT NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES lesson(id)
);

-- ---- Component link tables ----

-- word <-> character  (1..n characters per word, 0..n words per character)
CREATE TABLE word_character_link (
    word_id TEXT NOT NULL,
    character_id TEXT NOT NULL,
    character_order INTEGER NOT NULL,
    token_text TEXT NOT NULL,
    PRIMARY KEY (word_id, character_order),
    FOREIGN KEY (word_id) REFERENCES word(id),
    FOREIGN KEY (character_id) REFERENCES character(id)
);

-- passage <-> word  (tokenizer backfill — populated post-migration by tokenizer)
CREATE TABLE passage_word_link (
    passage_id TEXT NOT NULL,
    word_id TEXT NOT NULL,
    token_order INTEGER NOT NULL,
    token_text TEXT NOT NULL,
    PRIMARY KEY (passage_id, token_order),
    FOREIGN KEY (passage_id) REFERENCES passage(id),
    FOREIGN KEY (word_id) REFERENCES word(id)
);

-- word -> passage  (example_sentence on word, 0..n)
CREATE TABLE word_passage_link (
    word_id TEXT NOT NULL,
    passage_id TEXT NOT NULL,
    PRIMARY KEY (word_id, passage_id),
    FOREIGN KEY (word_id) REFERENCES word(id),
    FOREIGN KEY (passage_id) REFERENCES passage(id)
);

-- character -> word  (example_word on character, 0..n)
CREATE TABLE character_word_link (
    character_id TEXT NOT NULL,
    word_id TEXT NOT NULL,
    PRIMARY KEY (character_id, word_id),
    FOREIGN KEY (character_id) REFERENCES character(id),
    FOREIGN KEY (word_id) REFERENCES word(id)
);

-- ---- Feature link tables ----

-- vocabulary -> passage  (example_sentence)
CREATE TABLE vocabulary_example_sentence (
    vocabulary_id TEXT NOT NULL,
    passage_id TEXT NOT NULL,
    PRIMARY KEY (vocabulary_id, passage_id),
    FOREIGN KEY (vocabulary_id) REFERENCES vocabulary(id),
    FOREIGN KEY (passage_id) REFERENCES passage(id)
);

-- calligraphy -> word  (example_word)
CREATE TABLE calligraphy_example_word (
    calligraphy_id TEXT NOT NULL,
    word_id TEXT NOT NULL,
    PRIMARY KEY (calligraphy_id, word_id),
    FOREIGN KEY (calligraphy_id) REFERENCES calligraphy(id),
    FOREIGN KEY (word_id) REFERENCES word(id)
);

-- calligraphy -> passage  (example_sentence)
CREATE TABLE calligraphy_example_sentence (
    calligraphy_id TEXT NOT NULL,
    passage_id TEXT NOT NULL,
    PRIMARY KEY (calligraphy_id, passage_id),
    FOREIGN KEY (calligraphy_id) REFERENCES calligraphy(id),
    FOREIGN KEY (passage_id) REFERENCES passage(id)
);

-- grammar -> word  (example_word)
CREATE TABLE grammar_example_word (
    grammar_id TEXT NOT NULL,
    word_id TEXT NOT NULL,
    PRIMARY KEY (grammar_id, word_id),
    FOREIGN KEY (grammar_id) REFERENCES grammar(id),
    FOREIGN KEY (word_id) REFERENCES word(id)
);

-- grammar -> passage  (example_sentence)
CREATE TABLE grammar_example_sentence (
    grammar_id TEXT NOT NULL,
    passage_id TEXT NOT NULL,
    PRIMARY KEY (grammar_id, passage_id),
    FOREIGN KEY (grammar_id) REFERENCES grammar(id),
    FOREIGN KEY (passage_id) REFERENCES passage(id)
);

-- exercise -> vocabulary  (related_voc)
CREATE TABLE exercise_vocabulary_link (
    exercise_id TEXT NOT NULL,
    vocabulary_id TEXT NOT NULL,
    PRIMARY KEY (exercise_id, vocabulary_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(id),
    FOREIGN KEY (vocabulary_id) REFERENCES vocabulary(id)
);

-- exercise -> grammar  (related_gram)
CREATE TABLE exercise_grammar_link (
    exercise_id TEXT NOT NULL,
    grammar_id TEXT NOT NULL,
    PRIMARY KEY (exercise_id, grammar_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(id),
    FOREIGN KEY (grammar_id) REFERENCES grammar(id)
);

-- exercise -> calligraphy  (related_call)
CREATE TABLE exercise_calligraphy_link (
    exercise_id TEXT NOT NULL,
    calligraphy_id TEXT NOT NULL,
    PRIMARY KEY (exercise_id, calligraphy_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(id),
    FOREIGN KEY (calligraphy_id) REFERENCES calligraphy(id)
);

-- ---- Polymorphic source/tag junction tables ----
-- FIX: added CHECK constraints so element_type typos are caught at insert time.
-- element_type values: 'language','lesson','word','character','passage',
--                      'vocabulary','grammar','calligraphy','exercise'

CREATE TABLE element_source (
    element_type TEXT NOT NULL CHECK(element_type IN (
        'language','lesson','word','character','passage',
        'vocabulary','grammar','calligraphy','exercise' 
    )),
    element_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (element_type, element_id, source_id),
    FOREIGN KEY (source_id) REFERENCES source(id)
);

CREATE TABLE element_tag (
    element_type TEXT NOT NULL CHECK(element_type IN (
        'language','lesson','word','character','passage',
        'vocabulary','grammar','calligraphy','exercise'
    )),
    element_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (element_type, element_id, tag_id),
    FOREIGN KEY (tag_id) REFERENCES tag(id)
);

-- ============================================================================
-- 3) Seed system user, preferences, and sources
-- ============================================================================

INSERT INTO user (id, username, day_streak)
VALUES ('user_0', 'system', 0);

INSERT INTO user_preferences (id, user_id, native_language_iso639_2, learning_goals, preferred_exercise_types)
VALUES ('preference_0', 'user_0', '["eng","fra"]', '', '[]');

INSERT INTO source (id, user_id, title, date, description, source_type) VALUES
    ('source_0',  'user_0', 'AI generated',  DATE('now'),
     'Created by migration tokenizer extraction', 'ai'),
    ('source_1', 'user_0', 'Nihaoma?', DATE('now'),
     'Cours de chinois issus de mon manuel français A1/A2', 'manual'),
    ('source_2', 'user_0', 'Spektrum Deutsch A1', DATE('now'),
     'German course material from Spektrum A1', 'manual');

-- ============================================================================
-- 4) Language and lesson
-- ============================================================================

INSERT INTO language (id, user_id, description, level, score, last_seen_at, name, native_name, flag)
SELECT id, 'user_0', description, level, score, last_seen, name, native_name, flag
FROM old_language;

CREATE TEMP TABLE lesson_id_map AS
SELECT id AS old_id,
       'lesson_L' || ROW_NUMBER() OVER (ORDER BY id) AS new_id
FROM old_unit;

-- FIX: lesson now includes user_id
INSERT INTO lesson (id, user_id, description, level, score, last_seen_at, title, language_id)
SELECT lm.new_id, 'user_0', ou.description, ou.level, ou.score, ou.last_seen, ou.title, ou.language_id
FROM old_unit ou
JOIN lesson_id_map lm ON ou.id = lm.old_id;

-- Seed strengths_and_weaknesses: one row per (user × language × element_type)
INSERT INTO strengths_and_weaknesses (id, user_id, language_id, language_name, element_type)
SELECT
    'Saw_' || ol.id || '_' || et.element_type,
    'user_0',
    ol.id,
    ol.name,
    et.element_type
FROM old_language ol
CROSS JOIN (
    SELECT 'vocabulary'  AS element_type UNION ALL
    SELECT 'grammar'                     UNION ALL
    SELECT 'calligraphy'                 UNION ALL
    SELECT 'exercise'
) et;

INSERT INTO element_source (element_type, element_id, source_id)
SELECT 'language', id, 'source_1' FROM language
UNION ALL
SELECT 'lesson',   id, 'source_1' FROM lesson;

-- ============================================================================
-- 5) Word backfill
-- ============================================================================

CREATE TEMP TABLE word_usage_language AS
SELECT DISTINCT ov.word_id AS old_word_id, ou.language_id
FROM old_vocabulary ov
JOIN old_unit ou ON ov.unit_id = ou.id
UNION
SELECT DISTINCT oc.example_word_id AS old_word_id, ou.language_id
FROM old_calligraphy oc
JOIN old_unit ou ON oc.unit_id = ou.id
WHERE oc.example_word_id IS NOT NULL;

-- FIX: deduplicate across both arms of the UNION before assigning new IDs
--      to prevent a word appearing in word_usage_language *and* the orphan
--      fallback from generating two rows with different new_ids.
CREATE TEMP TABLE word_id_map AS
SELECT
    deduped.old_word_id,
    deduped.language_id,
    'word_W' || ROW_NUMBER() OVER (ORDER BY deduped.language_id, deduped.old_word_id) AS new_id
FROM (
    SELECT old_word_id, language_id
    FROM word_usage_language
    UNION  -- UNION deduplicates; do not use UNION ALL here
    SELECT ow.id AS old_word_id,
           (SELECT id FROM old_language ORDER BY id LIMIT 1) AS language_id
    FROM old_word ow
    WHERE NOT EXISTS (
        SELECT 1 FROM word_usage_language wul WHERE wul.old_word_id = ow.id
    )
) AS deduped;

INSERT INTO word (
    id, language_id, word, translation, phonetic,
    word_type, word_gender, image_files, audio_files, difficulty, created_at, last_seen_at
)
SELECT
    wm.new_id, wm.language_id, ow.word,
    COALESCE(NULLIF(ow.translation, ''), ''),
    ow.phonetic, ow.type, ow.gender,
    COALESCE(ow.image_files, '[]'),
    COALESCE(ow.audio_files, '[]'),
    0.5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM word_id_map wm
JOIN old_word ow ON ow.id = wm.old_word_id;

INSERT INTO element_source (element_type, element_id, source_id)
SELECT 'word', wm.new_id, 'source_1'
FROM word_id_map wm;

-- ============================================================================
-- 6) Passage backfill + word links
-- ============================================================================

CREATE TEMP TABLE passage_usage_language AS
SELECT DISTINCT op.id AS old_passage_id, ou.language_id
FROM old_passage op
JOIN old_vocabulary ov ON op.vocabulary_id = ov.id
JOIN old_unit ou ON ov.unit_id = ou.id
WHERE op.vocabulary_id IS NOT NULL
UNION
SELECT DISTINCT op.id AS old_passage_id, ou.language_id
FROM old_passage op
JOIN old_grammar og ON op.grammar_id = og.id
JOIN old_unit ou ON og.unit_id = ou.id
WHERE op.grammar_id IS NOT NULL;

CREATE TEMP TABLE passage_id_map AS
SELECT
    src.old_passage_id,
    src.language_id,
    'passage_P' || ROW_NUMBER() OVER (ORDER BY src.language_id, src.old_passage_id) AS new_id
FROM (
    SELECT old_passage_id, language_id
    FROM passage_usage_language
    UNION  -- UNION deduplicates
    SELECT op.id AS old_passage_id,
           (SELECT id FROM old_language ORDER BY id LIMIT 1) AS language_id
    FROM old_passage op
    WHERE NOT EXISTS (
        SELECT 1 FROM passage_usage_language pul WHERE pul.old_passage_id = op.id
    )
) AS src;

INSERT INTO passage (
    id, language_id, text, translation,
    image_files, audio_files, difficulty, created_at, last_seen_at
)
SELECT
    pm.new_id, pm.language_id, op.text,
    COALESCE(NULLIF(op.translation, ''), ''),
    COALESCE(op.image_files, '[]'),
    COALESCE(op.audio_files, '[]'),
    0.5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM passage_id_map pm
JOIN old_passage op ON op.id = pm.old_passage_id;

INSERT INTO element_source (element_type, element_id, source_id)
SELECT 'passage', pm.new_id, 'source_1'
FROM passage_id_map pm;

-- NOTE: passage_word_link, word_passage_link, and word_character_link are
--       intentionally left empty here. They require a tokenizer pass over the
--       migrated text that runs as a separate post-migration job. The tables
--       are created and ready to receive data.

-- ============================================================================
-- 7) Character backfill + word-character links (CJK only)
-- ============================================================================

CREATE TEMP TABLE character_usage_language AS
SELECT DISTINCT oc.character_id AS old_character_id, ou.language_id
FROM old_calligraphy oc
JOIN old_unit ou ON oc.unit_id = ou.id;

CREATE TEMP TABLE character_id_map AS
SELECT
    src.old_character_id,
    src.language_id,
    'char_C' || ROW_NUMBER() OVER (ORDER BY src.language_id, src.old_character_id) AS new_id
FROM (
    SELECT old_character_id, language_id
    FROM character_usage_language
    UNION  -- UNION deduplicates
    SELECT oc.id AS old_character_id,
           (SELECT id FROM old_language ORDER BY id LIMIT 1) AS language_id
    FROM old_character oc
    WHERE NOT EXISTS (
        SELECT 1 FROM character_usage_language cul WHERE cul.old_character_id = oc.id
    )
) AS src;

INSERT INTO character (
    id, language_id, character, phonetic, meaning,
    radical, strokes, image_files, audio_files, difficulty, created_at, last_seen_at
)
SELECT
    cm.new_id, cm.language_id, oc.character, oc.phonetic, oc.meaning,
    oc.radical, oc.strokes,
    COALESCE(oc.image_files, '[]'),
    COALESCE(oc.audio_files, '[]'),
    0.5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM character_id_map cm
JOIN old_character oc ON oc.id = cm.old_character_id;

INSERT INTO element_source (element_type, element_id, source_id)
SELECT 'character', cm.new_id, 'source_1'
FROM character_id_map cm;

-- NOTE: character_word_link is left empty — requires the post-migration
--       tokenizer to decompose words into their constituent characters.

-- ============================================================================
-- 8) Feature backfill
-- ============================================================================

-- FIX: carry over image_files, and audio_files from old_vocabulary
INSERT INTO vocabulary (
    id, image_files, audio_files, score,
    last_seen_at, lesson_id, difficulty, word_id
)
SELECT
    ov.id,
    COALESCE(ov.image_files, '[]'),
    COALESCE(ov.audio_files, '[]'),
    ov.score,
    ov.last_seen,
    lm.new_id,
    0.5,
    wm.new_id
FROM old_vocabulary ov
JOIN old_unit ou ON ov.unit_id = ou.id
JOIN lesson_id_map lm ON ou.id = lm.old_id
JOIN word_id_map wm ON wm.old_word_id = ov.word_id AND wm.language_id = ou.language_id;

INSERT INTO grammar (id, image_files, audio_files, score, last_seen_at, lesson_id, difficulty, title, explanation)
SELECT og.id,
    COALESCE(og.image_files, '[]'),
    COALESCE(og.audio_files, '[]'),
    og.score, og.last_seen, lm.new_id, 0.5, og.title, og.explanation
FROM old_grammar og
JOIN old_unit ou ON og.unit_id = ou.id
JOIN lesson_id_map lm ON ou.id = lm.old_id;

INSERT INTO calligraphy (id, image_files, audio_files, score, last_seen_at, lesson_id, difficulty, character_id)
SELECT oc.id,
    COALESCE(oc.image_files, '[]'),
    COALESCE(oc.audio_files, '[]'),
    oc.score, oc.last_seen, lm.new_id, 0.5, cm.new_id
FROM old_calligraphy oc
JOIN old_unit ou ON oc.unit_id = ou.id
JOIN lesson_id_map lm ON ou.id = lm.old_id
JOIN character_id_map cm ON cm.old_character_id = oc.character_id AND cm.language_id = ou.language_id;

-- Migrate calligraphy example_word → calligraphy_example_word
INSERT INTO calligraphy_example_word (calligraphy_id, word_id)
SELECT oc.id, wm.new_id
FROM old_calligraphy oc
JOIN old_unit ou ON oc.unit_id = ou.id
JOIN word_id_map wm ON wm.old_word_id = oc.example_word_id AND wm.language_id = ou.language_id
WHERE oc.example_word_id IS NOT NULL;

INSERT INTO exercise (
    id, image_files, audio_files, score, last_seen_at, lesson_id, difficulty,
    exercise_type, question, answer, text_support
)
SELECT oe.id,
    COALESCE(oe.image_files, '[]'),
    COALESCE(oe.audio_files, '[]'),
    oe.score, oe.last_seen, lm.new_id, 0.5,
    oe.exercise_type, oe.question, oe.answer, oe.text_support
FROM old_exercise oe
JOIN old_unit ou ON oe.unit_id = ou.id
JOIN lesson_id_map lm ON ou.id = lm.old_id;

-- Migrate old_passage.vocabulary_id → vocabulary_example_sentence
INSERT INTO vocabulary_example_sentence (vocabulary_id, passage_id)
SELECT op.vocabulary_id, pm.new_id
FROM old_passage op
JOIN old_vocabulary ov ON op.vocabulary_id = ov.id
JOIN old_unit ou ON ov.unit_id = ou.id
JOIN passage_id_map pm ON pm.old_passage_id = op.id AND pm.language_id = ou.language_id
WHERE op.vocabulary_id IS NOT NULL;

-- Migrate old_passage.grammar_id → grammar_example_sentence
INSERT INTO grammar_example_sentence (grammar_id, passage_id)
SELECT op.grammar_id, pm.new_id
FROM old_passage op
JOIN old_grammar og ON op.grammar_id = og.id
JOIN old_unit ou ON og.unit_id = ou.id
JOIN passage_id_map pm ON pm.old_passage_id = op.id AND pm.language_id = ou.language_id
WHERE op.grammar_id IS NOT NULL;

-- NOTE: vocabulary_grammar_link and vocabulary_calligraphy_link are left
--       empty — no equivalent relationship existed in the old schema.
--       Populate via future feature work.

INSERT INTO element_source (element_type, element_id, source_id)
SELECT 'vocabulary',  id, 'source_0' FROM vocabulary
UNION ALL SELECT 'grammar',     id, 'source_0' FROM grammar
UNION ALL SELECT 'calligraphy', id, 'source_0' FROM calligraphy
UNION ALL SELECT 'exercise',    id, 'source_0' FROM exercise;

-- ============================================================================
-- 9) Cleanup
-- ============================================================================

DROP TABLE old_language;
DROP TABLE old_unit;
DROP TABLE old_word;
DROP TABLE old_character;
DROP TABLE old_passage;
DROP TABLE old_vocabulary;
DROP TABLE old_grammar;
DROP TABLE old_calligraphy;
DROP TABLE old_exercise;

COMMIT;
PRAGMA foreign_keys = ON;

-- ============================================================================
-- 10) Verification
-- ============================================================================

SELECT 'Migration complete' AS status;
SELECT tbl, rows FROM (
    SELECT 'user'                       AS tbl, COUNT(*) AS rows FROM user
    UNION ALL SELECT 'user_preferences',           COUNT(*) FROM user_preferences
    UNION ALL SELECT 'source',                     COUNT(*) FROM source
    UNION ALL SELECT 'tag',                        COUNT(*) FROM tag
    UNION ALL SELECT 'strengths_and_weaknesses',   COUNT(*) FROM strengths_and_weaknesses
    UNION ALL SELECT 'progress_tracking',          COUNT(*) FROM progress_tracking
    UNION ALL SELECT 'language',                   COUNT(*) FROM language
    UNION ALL SELECT 'lesson',                     COUNT(*) FROM lesson
    UNION ALL SELECT 'word',                       COUNT(*) FROM word
    UNION ALL SELECT 'character',                  COUNT(*) FROM character
    UNION ALL SELECT 'passage',                    COUNT(*) FROM passage
    UNION ALL SELECT 'vocabulary',                 COUNT(*) FROM vocabulary
    UNION ALL SELECT 'grammar',                    COUNT(*) FROM grammar
    UNION ALL SELECT 'calligraphy',                COUNT(*) FROM calligraphy
    UNION ALL SELECT 'exercise',                   COUNT(*) FROM exercise
    UNION ALL SELECT 'element_source',             COUNT(*) FROM element_source
    UNION ALL SELECT 'element_tag',                COUNT(*) FROM element_tag
    UNION ALL SELECT 'passage_word_link',          COUNT(*) FROM passage_word_link
    UNION ALL SELECT 'word_character_link',        COUNT(*) FROM word_character_link
    UNION ALL SELECT 'word_passage_link',          COUNT(*) FROM word_passage_link
    UNION ALL SELECT 'character_word_link',        COUNT(*) FROM character_word_link
    UNION ALL SELECT 'vocabulary_example_sentence',    COUNT(*) FROM vocabulary_example_sentence
    UNION ALL SELECT 'calligraphy_example_word',      COUNT(*) FROM calligraphy_example_word
    UNION ALL SELECT 'calligraphy_example_sentence',   COUNT(*) FROM calligraphy_example_sentence
    UNION ALL SELECT 'grammar_example_word',         COUNT(*) FROM grammar_example_word
    UNION ALL SELECT 'grammar_example_sentence',       COUNT(*) FROM grammar_example_sentence
    UNION ALL SELECT 'exercise_vocabulary_link',  COUNT(*) FROM exercise_vocabulary_link
    UNION ALL SELECT 'exercise_grammar_link',      COUNT(*) FROM exercise_grammar_link
    UNION ALL SELECT 'exercise_calligraphy_link',  COUNT(*) FROM exercise_calligraphy_link
);