# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
from typing import List

from scrapy.exceptions import DropItem

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter, is_item

from oxford.sqlite3_orm import SqliteORM
from oxford.models import WORDS_TABLE, DEFINITIONS_TABLE


class OxfordPipeline:
    def process_item(self, item, spider):
        return item


def print_header(message: str, divider: str = "-", length: int = 45) -> None:
    print(divider * length)
    print(message.center(length))
    print(divider * length)


class SaveWordPipeline:
    def __init__(self):
        print_header("SaveWordPipeline: Enabled")
        self.sqlite = SqliteORM("dictionary.db")
        self.last_word_id = None
        self.create_words_table(WORDS_TABLE)

    def create_words_table(self, table):
        self.sqlite.connect()
        self.sqlite.create_table(table)
        self.sqlite.try_to_commit_and_close()

    def process_item(self, item, spider):
        if not self.is_word_item(item):
            return item

        self.sqlite.connect()
        self.save_word(item)
        self.sqlite.try_to_commit_and_close()
        return item

    def save_word(self, item):
        self.last_word_id = self.sqlite.insert_word(item)
        print_header(f"WordItem saved into {self.sqlite.db_name}")

    def is_word_item(self, item):
        return item.get("word_type")


class SaveDefinitionPipeline:
    def __init__(self):
        print_header("SaveDefinitionPipeline: Enabled")
        self.word_id = None
        self.sqlite = SqliteORM("dictionary.db")
        self.create_definitions_table(DEFINITIONS_TABLE)

    def create_definitions_table(self, table):
        self.sqlite.connect()
        self.sqlite.create_table(table)
        self.sqlite.try_to_commit_and_close()

    def process_item(self, item, spider):
        if not self.is_definition_item(item):
            return item

        adapter = ItemAdapter(item)

        self.sqlite.connect()
        self.word_id = self.get_word_id(spider)
        adapter["word_id"] = self.word_id

        self.save_definitions(adapter)
        self.sqlite.try_to_commit_and_close()
        return adapter

    def save_definitions(self, item):
        definitions = self.listfy_data(item)
        self.sqlite.insert_many_definitions(definitions)
        print_header(f"DefinitionItem saved into {self.sqlite.db_name}")

    def is_definition_item(self, item):
        return item.get("def_type")

    def get_word_id(self, spider):
        self.sqlite.connect()
        print_header(f"spider.word: {spider.word}")
        print_header(f"spider.word_type: {spider.word_type}")
        word_row = self.sqlite.query_word(spider.word, spider.word_type)
        print_header(f"word_row: {word_row}")
        return word_row[1]

    def listfy_data(self, data: dict) -> List[tuple]:
        """
        data: {"defs": [def0, def1, ..., defN], "cefr": [cefr0, cefr1, ..., cefrN]}
        returns:
            [(def0, cefr0), (def1, cefr1), ..., (defN, cefrN)]
        """
        data_list = []
        for i, item in enumerate(data.get("definition")):
            data_list.append(
                (
                    data.get("definition")[i],
                    data.get("cefr")[i],
                    data.get("grammar")[i],
                    data.get("def_type")[i],
                    data.get("context")[i],
                    data.get("labels")[i],
                    data.get("variants")[i],
                    data.get("use")[i],
                    data.get("synonyms")[i],
                    data.get("word_id"),
                )
            )
        print(data_list)
        return data_list


class DuplicatesWordsSQLitePipeline:
    def __init__(self):
        print_header("DuplicatesWordsSQLitePipeline: Enabled")
        self.words_seen = set()
        self.sqlite = SqliteORM("dictionary.db")

    def process_item(self, item, spider):
        self.sqlite.connect()
        adapter = ItemAdapter(item)

        if not self.is_word_item(adapter):
            return item

        if self.word_exists(adapter):
            self.sqlite.close()
            raise DropItem(f"Duplicate word found: {item['word']}")
        else:
            self.words_seen.add(adapter["word"])
            self.sqlite.close()
            return item

    def is_word_item(self, item):
        return item.get("word_type")

    def word_exists(self, item):
        return self.sqlite.query_word(item["word"], item["word_type"])


class DuplicatesDefinitionsSQLitePipeline:
    def __init__(self):
        print_header("DuplicatesDefinitionssSQLitePipeline: Enabled")
        self.definitions_seen = set()
        self.sqlite = SqliteORM("dictionary.db")

    def process_item(self, item, spider):
        self.sqlite.connect()
        adapter = ItemAdapter(item)

        if not self.is_definition_item(adapter):
            return item

        if self.definition_exists(adapter):
            self.sqlite.close()
            raise DropItem(f"Duplicate definition found: {item['definition']}")
        else:
            self.definitions_seen.add(adapter["definition"])
            self.sqlite.close()
            return item

    def is_definition_item(self, item):
        return item.get("def_type")

    def definition_exists(self, item):
        return self.sqlite.query_definition(item["definition"])


class DuplicatesPipeline:
    def __init__(self):
        print_header("DuplicatesPipeline: Enabled")
        self.words_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if self.is_word_seen(item):
            raise DropItem(f"Duplicate word found: {item['word']}")
        else:
            self.words_seen.add(adapter["word"])
            return item

    def is_word_seen(self, item):
        return is_item(item) and item["word"] in self.words_seen


class JsonWriterPipeline:
    def __init__(self):
        print_header("JsonWriterPipeline: Enabled")

    def open_spider(self, spider):
        self.file = open("dictionary.jl", "w", encoding="utf8")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
