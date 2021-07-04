# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

from scrapy.exceptions import DropItem

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from oxford.sqlite3_orm import SqliteORM
from oxford.models import WORDS_TABLE


class OxfordPipeline:
    def process_item(self, item, spider):
        return item


class SaveWordPipeline:
    def __init__(self):
        self.print_header()
        self.sqlite = SqliteORM("dictionary.db")

    def process_item(self, item, spider):
        self.sqlite.connect()
        self.sqlite.create_table(WORDS_TABLE)

        item["word"] = "default word"
        self.sqlite.insert_word(item)
        self.sqlite.try_to_commit_and_close()
        self.print_header("Item Saved")
        return item

    def print_header(self, msg: str = "SaveWordPipeline"):
        print("-" * 25)
        print(msg.center(25))
        print("-" * 25)


class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["word"] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter["word"])
            return item


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open("dict.jl", "w", encoding="utf8")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
