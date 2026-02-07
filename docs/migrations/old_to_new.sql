-- Migration plan: old_models.py -> new models/
-- Target DB: SQLite
-- This script renames old tables, creates new tables, migrates data with new ID format

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

-- 1) Preserve old tables
ALTER TABLE language RENAME TO old_language;
ALTER TABLE unit RENAME TO old_unit;
ALTER TABLE calligraphy_character RENAME TO old_calligraphy_character;
ALTER TABLE grammar_rule RENAME TO old_grammar_rule;
ALTER TABLE vocabulary RENAME TO old_vocabulary;
ALTER TABLE exercises RENAME TO old_exercises;

-- 2) Create new tables (aligned to new SQLAlchemy models)
CREATE TABLE language (
    id TEXT PRIMARY KEY,
    score INTEGER DEFAULT 0,
    last_seen DATE,
    name TEXT,
    native_name TEXT,
    level TEXT,
    description TEXT DEFAULT '',
    flag TEXT DEFAULT '',
    current_unit TEXT
);

CREATE TABLE unit (
    id TEXT PRIMARY KEY,
    score INTEGER DEFAULT 0,
    last_seen DATE,
    title TEXT,
    description TEXT,
    level TEXT,
    language_id TEXT NOT NULL,
    FOREIGN KEY (language_id) REFERENCES language(id)
);

CREATE TABLE character (
    id TEXT PRIMARY KEY,
    image_files JSON DEFAULT '[]',
    audio_files JSON DEFAULT '[]',
    character TEXT NOT NULL,
    phonetic TEXT NOT NULL,
    meaning TEXT,
    radical TEXT,
    strokes INTEGER
);

CREATE TABLE word (
    id TEXT PRIMARY KEY,
    image_files JSON DEFAULT '[]',
    audio_files JSON DEFAULT '[]',
    word TEXT NOT NULL,
    translation TEXT NOT NULL,
    phonetic TEXT,
    type TEXT
);

CREATE TABLE passage (
    id TEXT PRIMARY KEY,
    image_files JSON DEFAULT '[]',
    audio_files JSON DEFAULT '[]',
    text TEXT NOT NULL,
    translation TEXT NOT NULL,
    vocabulary_id TEXT,
    grammar_id TEXT,
    FOREIGN KEY (vocabulary_id) REFERENCES vocabulary(id),
    FOREIGN KEY (grammar_id) REFERENCES grammar(id)
);

CREATE TABLE vocabulary (
    id TEXT PRIMARY KEY,
    score INTEGER DEFAULT 0,
    last_seen DATE,
    unit_id TEXT NOT NULL,
    image_files JSON DEFAULT '[]',
    audio_files JSON DEFAULT '[]',
    word_id TEXT NOT NULL,
    FOREIGN KEY (unit_id) REFERENCES unit(id),
    FOREIGN KEY (word_id) REFERENCES word(id)
);

CREATE TABLE grammar (
    id TEXT PRIMARY KEY,
    score INTEGER DEFAULT 0,
    last_seen DATE,
    unit_id TEXT NOT NULL,
    image_files JSON DEFAULT '[]',
    audio_files JSON DEFAULT '[]',
    title TEXT,
    explanation TEXT,
    FOREIGN KEY (unit_id) REFERENCES unit(id)
);

CREATE TABLE calligraphy (
    id TEXT PRIMARY KEY,
    score INTEGER DEFAULT 0,
    last_seen DATE,
    unit_id TEXT NOT NULL,
    image_files JSON DEFAULT '[]',
    audio_files JSON DEFAULT '[]',
    character_id TEXT NOT NULL,
    example_word_id TEXT,
    FOREIGN KEY (unit_id) REFERENCES unit(id),
    FOREIGN KEY (character_id) REFERENCES character(id),
    FOREIGN KEY (example_word_id) REFERENCES word(id)
);

CREATE TABLE exercise (
    id TEXT PRIMARY KEY,
    score INTEGER DEFAULT 0,
    last_seen DATE,
    unit_id TEXT NOT NULL,
    image_files JSON DEFAULT '[]',
    audio_files JSON DEFAULT '[]',
    exercise_type TEXT,
    question TEXT,
    answer TEXT,
    text_support TEXT DEFAULT '',
    vocabulary_ids JSON DEFAULT '[]',
    calligraphy_ids JSON DEFAULT '[]',
    grammar_ids JSON DEFAULT '[]',
    FOREIGN KEY (unit_id) REFERENCES unit(id)
);

-- 3) Create ID mapping tables with new sequential IDs
CREATE TEMP TABLE language_id_map AS
SELECT id AS old_id, 'lang_L' || ROW_NUMBER() OVER (ORDER BY ROWID) AS new_id
FROM old_language;

CREATE TEMP TABLE unit_id_map AS
SELECT id AS old_id, 'unit_U' || ROW_NUMBER() OVER (ORDER BY ROWID) AS new_id
FROM old_unit;

CREATE TEMP TABLE character_id_map AS
SELECT id AS old_id, 'char_C' || ROW_NUMBER() OVER (ORDER BY ROWID) AS new_id
FROM old_calligraphy_character;

CREATE TEMP TABLE word_id_map AS
SELECT word, 'word_W' || ROW_NUMBER() OVER (ORDER BY min_rowid) AS new_id
FROM (
    SELECT word, MIN(ROWID) AS min_rowid
    FROM old_vocabulary
    GROUP BY word
);

CREATE TEMP TABLE grammar_id_map AS
SELECT id AS old_id, 'gram_G' || ROW_NUMBER() OVER (ORDER BY ROWID) AS new_id
FROM old_grammar_rule;

CREATE TEMP TABLE vocabulary_id_map AS
SELECT id AS old_id, 'voc_V' || ROW_NUMBER() OVER (ORDER BY ROWID) AS new_id
FROM old_vocabulary;

CREATE TEMP TABLE calligraphy_id_map AS
SELECT id AS old_id, 'call_C' || ROW_NUMBER() OVER (ORDER BY ROWID) AS new_id
FROM old_calligraphy_character;

CREATE TEMP TABLE exercise_id_map AS
SELECT id AS old_id, 'ex_E' || ROW_NUMBER() OVER (ORDER BY ROWID) AS new_id
FROM old_exercises;

-- 4) Insert Units FIRST (before Languages, to avoid FK issues with current_unit)
INSERT INTO unit (id, score, last_seen, title, description, level, language_id)
SELECT um.new_id, ou.score, ou.last_seen, ou.title, ou.description, ou.level, lm.new_id
FROM old_unit ou
JOIN unit_id_map um ON ou.id = um.old_id
JOIN language_id_map lm ON ou.language_id = lm.old_id;

-- 5) Insert Languages with mapped current_unit
INSERT INTO language (id, score, last_seen, name, native_name, level, description, flag, current_unit)
SELECT lm.new_id, ol.score, ol.last_seen, ol.name, ol.native_name, ol.level, ol.description, ol.flag,
       (SELECT new_id FROM unit_id_map WHERE old_id = ol.current_unit)
FROM old_language ol
JOIN language_id_map lm ON ol.id = lm.old_id;

-- 6) Insert Characters
INSERT INTO character (id, character, phonetic, meaning, radical, strokes, image_files, audio_files)
SELECT cm.new_id, oc.character, oc.phonetic, oc.meaning, oc.components, NULL, '[]', '[]'
FROM old_calligraphy_character oc
JOIN character_id_map cm ON oc.id = cm.old_id;

-- 7) Insert Words (deduplicated from vocabulary)
INSERT INTO word (id, word, translation, phonetic, type, image_files, audio_files)
SELECT wm.new_id, ov.word, ov.translation, ov.phonetic, ov.type, '[]', '[]'
FROM (
    SELECT word, translation, phonetic, type, MIN(ROWID) AS min_rowid
    FROM old_vocabulary
    GROUP BY word
) AS voc_dedup
JOIN old_vocabulary ov ON ov.ROWID = voc_dedup.min_rowid
JOIN word_id_map wm ON ov.word = wm.word;

-- 8) Add words from calligraphy example_word (if not already present)
INSERT INTO word (id, word, translation, phonetic, type, image_files, audio_files)
SELECT 'word_W' || (ROW_NUMBER() OVER (ORDER BY c.ROWID) + (SELECT COUNT(*) FROM word)),
       c.example_word, '', NULL, NULL, '[]', '[]'
FROM (
    SELECT DISTINCT example_word, ROWID
    FROM old_calligraphy_character
    WHERE example_word IS NOT NULL 
      AND trim(example_word) <> ''
      AND example_word NOT IN (SELECT word FROM word_id_map)
) c;

-- Update word_id_map with new example words
INSERT INTO word_id_map (word, new_id)
SELECT w.word, w.id
FROM word w
WHERE w.id NOT IN (SELECT new_id FROM word_id_map);

-- 9) Insert Grammar
INSERT INTO grammar (id, score, last_seen, unit_id, title, explanation, image_files, audio_files)
SELECT gm.new_id, og.score, og.last_seen, um.new_id, og.title, og.explanation, '[]', '[]'
FROM old_grammar_rule og
JOIN grammar_id_map gm ON og.id = gm.old_id  -- ✅ FIXED: was gm.new_id
JOIN unit_id_map um ON og.unit_id = um.old_id;

-- 10) Insert Vocabulary
INSERT INTO vocabulary (id, score, last_seen, unit_id, word_id, image_files, audio_files)
SELECT vm.new_id, ov.score, ov.last_seen, um.new_id, wm.new_id, '[]', '[]'
FROM old_vocabulary ov
JOIN vocabulary_id_map vm ON ov.id = vm.old_id
JOIN unit_id_map um ON ov.unit_id = um.old_id
JOIN word_id_map wm ON ov.word = wm.word;

-- 11) Insert Passages from Vocabulary example_sentence
INSERT INTO passage (id, text, translation, vocabulary_id, grammar_id, image_files, audio_files)
SELECT 
    'pass_P' || ROW_NUMBER() OVER (ORDER BY vm.new_id),
    ov.example_sentence, 
    '', 
    vm.new_id, 
    NULL, 
    '[]', 
    '[]'
FROM old_vocabulary ov
JOIN vocabulary_id_map vm ON ov.id = vm.old_id
WHERE ov.example_sentence IS NOT NULL AND trim(ov.example_sentence) <> '';

-- 12) Insert Passages from Grammar learnable_sentence (continue sequence)
INSERT INTO passage (id, text, translation, vocabulary_id, grammar_id, image_files, audio_files)
SELECT 
    'pass_P' || (
        COALESCE((SELECT MAX(CAST(SUBSTR(id, 7) AS INTEGER)) FROM passage), 0) + 
        ROW_NUMBER() OVER (ORDER BY gm.new_id)
    ),
    og.learnable_sentence, 
    '', 
    NULL, 
    gm.new_id, 
    '[]', 
    '[]'
FROM old_grammar_rule og
JOIN grammar_id_map gm ON og.id = gm.old_id
WHERE og.learnable_sentence IS NOT NULL 
  AND trim(og.learnable_sentence) <> ''
  AND og.learnable_sentence NOT IN (SELECT text FROM passage);

-- 13) Insert Calligraphy
INSERT INTO calligraphy (id, score, last_seen, unit_id, character_id, example_word_id, image_files, audio_files)
SELECT cym.new_id, oc.score, oc.last_seen, um.new_id, cm.new_id,
       (SELECT new_id FROM word_id_map WHERE word = oc.example_word), '[]', '[]'
FROM old_calligraphy_character oc
JOIN calligraphy_id_map cym ON oc.id = cym.old_id
JOIN unit_id_map um ON oc.unit_id = um.old_id
JOIN character_id_map cm ON oc.id = cm.old_id;

-- 14) Insert Exercises with ID conversion and image extraction
INSERT INTO exercise (
    id, score, last_seen, unit_id,
    exercise_type, question, answer, text_support,
    vocabulary_ids, calligraphy_ids, grammar_ids,
    image_files, audio_files
)
SELECT 
    em.new_id, 
    oe.score, 
    oe.last_seen, 
    um.new_id,
    oe.exercise_type, 
    oe.question, 
    oe.answer, 
    -- Remove image_url tags AND the URL itself from text_support
    TRIM(
        SUBSTR(oe.support, 1, 
            CASE 
                WHEN INSTR(oe.support, '<image_url>') > 0 
                THEN INSTR(oe.support, '<image_url>') - 1
                ELSE LENGTH(oe.support)
            END
        ) ||
        CASE 
            WHEN INSTR(oe.support, '</image_url>') > 0 
            THEN SUBSTR(oe.support, INSTR(oe.support, '</image_url>') + 12)
            ELSE ''
        END
    ),
    -- Convert vocabulary IDs from associated_to.vocabulary
    COALESCE((
        SELECT json_group_array(vm.new_id)
        FROM json_each(COALESCE(json_extract(oe.associated_to, '$.vocabulary'), '[]')) je
        JOIN vocabulary_id_map vm ON vm.old_id = je.value
    ), '[]'),
    -- Convert calligraphy IDs from associated_to.characters
    COALESCE((
        SELECT json_group_array(cm.new_id)
        FROM json_each(COALESCE(json_extract(oe.associated_to, '$.characters'), '[]')) je
        JOIN calligraphy_id_map cm ON cm.old_id = je.value
    ), '[]'),
    -- Convert grammar IDs from associated_to.grammar
    COALESCE((
        SELECT json_group_array(gm.new_id)
        FROM json_each(COALESCE(json_extract(oe.associated_to, '$.grammar'), '[]')) je
        JOIN grammar_id_map gm ON gm.old_id = je.value
    ), '[]'),
    -- Extract image URL and convert path from /assets/images/ to /media/images/
    CASE 
        WHEN oe.support LIKE '%<image_url>%</image_url>%' THEN
            json_array(
                REPLACE(
                    SUBSTR(
                        oe.support,
                        INSTR(oe.support, '<image_url>') + 11,
                        INSTR(oe.support, '</image_url>') - INSTR(oe.support, '<image_url>') - 11
                    ),
                    'http://localhost:8000/assets/images/',
                    '/media/images/'
                )
            )
        ELSE '[]'
    END,
    '[]'
FROM old_exercises oe
JOIN exercise_id_map em ON oe.id = em.old_id
JOIN unit_id_map um ON oe.unit_id = um.old_id;

-- 15) Create migration log for reference
CREATE TABLE id_migration_log (
    table_name TEXT,
    old_id TEXT,
    new_id TEXT,
    migrated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO id_migration_log (table_name, old_id, new_id)
SELECT 'language', old_id, new_id FROM language_id_map
UNION ALL SELECT 'unit', old_id, new_id FROM unit_id_map
UNION ALL SELECT 'character', old_id, new_id FROM character_id_map
UNION ALL SELECT 'word', word AS old_id, new_id FROM word_id_map
UNION ALL SELECT 'grammar', old_id, new_id FROM grammar_id_map
UNION ALL SELECT 'vocabulary', old_id, new_id FROM vocabulary_id_map
UNION ALL SELECT 'calligraphy', old_id, new_id FROM calligraphy_id_map
UNION ALL SELECT 'exercise', old_id, new_id FROM exercise_id_map;

COMMIT;
PRAGMA foreign_keys=ON;

-- ============================================================================
-- VERIFICATION
-- ============================================================================

SELECT 'Migration Complete!' AS status;

-- Count comparison
SELECT 'Old Tables' AS source, 
       'language' AS table_name, COUNT(*) AS row_count FROM old_language
UNION ALL SELECT 'New Tables', 'language', COUNT(*) FROM language
UNION ALL SELECT 'Old Tables', 'unit', COUNT(*) FROM old_unit
UNION ALL SELECT 'New Tables', 'unit', COUNT(*) FROM unit
UNION ALL SELECT 'Old Tables', 'character', COUNT(*) FROM old_calligraphy_character
UNION ALL SELECT 'New Tables', 'character', COUNT(*) FROM character
UNION ALL SELECT 'Old Tables', 'vocabulary', COUNT(*) FROM old_vocabulary
UNION ALL SELECT 'New Tables', 'vocabulary', COUNT(*) FROM vocabulary
UNION ALL SELECT 'New Tables', 'word', COUNT(*) FROM word
UNION ALL SELECT 'Old Tables', 'grammar', COUNT(*) FROM old_grammar_rule
UNION ALL SELECT 'New Tables', 'grammar', COUNT(*) FROM grammar
UNION ALL SELECT 'Old Tables', 'calligraphy', COUNT(*) FROM old_calligraphy_character
UNION ALL SELECT 'New Tables', 'calligraphy', COUNT(*) FROM calligraphy
UNION ALL SELECT 'Old Tables', 'exercise', COUNT(*) FROM old_exercises
UNION ALL SELECT 'New Tables', 'exercise', COUNT(*) FROM exercise
UNION ALL SELECT 'New Tables', 'passage', COUNT(*) FROM passage
ORDER BY table_name, source;

-- Sample new IDs
SELECT 'Sample Language IDs:' AS info; SELECT id FROM language LIMIT 5;
SELECT 'Sample Unit IDs:' AS info; SELECT id FROM unit LIMIT 5;
SELECT 'Sample Word IDs:' AS info; SELECT id FROM word LIMIT 5;
SELECT 'Sample Vocabulary IDs:' AS info; SELECT id FROM vocabulary LIMIT 5;

-- Optional cleanup after verification:
DROP TABLE old_language;
DROP TABLE old_unit;
DROP TABLE old_calligraphy_character;
DROP TABLE old_grammar_rule;
DROP TABLE old_vocabulary;
DROP TABLE old_exercises;
DROP TABLE id_migration_log;