# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

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
        self.sqlite.connect()
        self.save_word(item)
        self.sqlite.try_to_commit_and_close()
        return item

    def save_word(self, item):
        self.last_word_id = self.sqlite.insert_word(item)
        print_header(f"WordItem saved into {self.sqlite.db_name}")


class SaveDefinitionPipeline:
    def __init__(self):
        print_header("SaveDefinitionPipeline: Enabled")
        self.sqlite = SqliteORM("dictionary.db")

    def process_item(self, item, spider):
        self.sqlite.connect()
        self.sqlite.create_table(DEFINITIONS_TABLE)
        self.save_definitions(item)
        return item

    def save_definitions(self, item):
        self.sqlite.insert_word(item)
        self.sqlite.try_to_commit_and_close()
        print_header(f"DefinitionItem saved into {self.sqlite.db_name}")


class DuplicatesWordsSQLitePipeline:
    def __init__(self):
        print_header("DuplicatesWordsSQLitePipeline: Enabled")
        self.words_seen = set()
        self.sqlite = SqliteORM("dictionary.db")

    def process_item(self, item, spider):
        self.sqlite.connect()
        adapter = ItemAdapter(item)

        if self.word_exists(adapter):
            self.sqlite.close()
            raise DropItem(f"Duplicate word found: {item['word']}")
        else:
            self.words_seen.add(adapter["word"])
            self.sqlite.close()
            return item

    def word_exists(self, item):
        return self.sqlite.query_word(item["word"], item["word_type"])


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
