# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

from scrapy.exceptions import DropItem

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class OxfordPipeline:
    def process_item(self, item, spider):
        return item


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
