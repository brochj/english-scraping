import sqlite3
from sqlite3 import Connection
from typing import Type


class SqliteORM:
    def __init__(self, db_name):
        self.db_name: str = db_name
        self.connection: Type[Connection] = None

    def connect(self) -> Type[Connection]:
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        self.connection.close()

    def rollback(self):
        self.connection.rollback()

    def try_to_commit_and_close(self):
        try:
            self.connection.commit()
        except:
            self.connection.rollback()
            raise
        finally:
            self.connection.close()

    def create_table(self, table: str) -> None:
        cursor = self.connection.cursor()
        cursor.execute(table)

    def insert_word(self, values: dict) -> None:
        cursor = self.connection.cursor()
        word = values.get("word")
        cefr = values.get("cefr")
        word_type = values.get("word_type")
        ipa_nam = values.get("ipa_nam")
        ipa_br = values.get("ipa_br")
        cursor.execute(
            "INSERT INTO words VALUES (NULL, ?, ?, ?, ?, ?)",
            (
                word,
                cefr,
                word_type,
                ipa_nam,
                ipa_br,
            ),
        )
        return cursor.lastrowid

    def insert_definition(self, values: dict) -> None:
        cursor = self.connection.cursor()

        definition = values.get("definition")
        cefr = values.get("cefr")
        grammar = values.get("grammar")
        def_type = values.get("def_type")
        context = values.get("context")
        labels = values.get("labels")
        variants = values.get("variants")
        use = values.get("use")
        synonyms = values.get("synonyms")
        examples = values.get("examples")
        word_id = values.get("word_id")
        cursor.execute(
            "INSERT INTO words VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                definition,
                cefr,
                grammar,
                def_type,
                context,
                labels,
                variants,
                use,
                synonyms,
                word_id,
            ),
        )

    def last_word_id_inserted(self, cursor):
        return cursor.lastrowid
        # cursor.execute(
        #     f"SELECT rowid, * FROM words WHERE word = {word} AND word_type = {word_type}"
        # )
        # return cursor.fetchone()

    def query_word(self, word, word_type):
        cursor = self.connection.cursor()
        cursor.execute(
            f"SELECT rowid, * FROM words WHERE word = '{word}' AND word_type = '{word_type}'"
        )
        return cursor.fetchone()
