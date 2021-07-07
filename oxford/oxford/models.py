WORDS_TABLE = """CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        cefr TEXT,
        word_type TEXT,
        ipa_nam TEXT,
        ipa_br TEXT
    )
"""


DEFINITIONS_TABLE = """CREATE TABLE IF NOT EXISTS definitions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        definition TEXT,
        cefr TEXT,
        grammar TEXT,
        def_type TEXT,
        context TEXT,
        labels TEXT,
        variants TEXT,
        use TEXT,
        synonyms TEXT,
        word_id INTEGER,
        FOREIGN KEY (word_id) REFERENCES words (id)
    )
"""


EXAMPLES_TABLE = """CREATE TABLE IF NOT EXISTS examples (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        example TEXT,
        context TEXT,
        labels TEXT,
        definition_id INTEGER,
        word_id INTEGER,
        FOREIGN KEY (definition_id) REFERENCES words (id)
        FOREIGN KEY (word_id) REFERENCES words (id)
    )
"""
