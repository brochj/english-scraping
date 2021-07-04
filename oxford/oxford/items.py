# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose
from w3lib.html import remove_tags


def remove_whitespace(text: str) -> str:
    return text.strip()


def get_word_level_from_url(url: str) -> str:
    return url[-2:]


def join_examples(examples: list) -> str:
    if examples == []:
        return "None"
    return " | ".join(examples)


def listfy_examples(examples: str) -> list:
    if examples == "None":
        return [[None]]
    return [examples.split(" | ")]


# fmt: off
class OxfordItem(scrapy.Item):  
    ipa_nam = scrapy.Field(
        input_processor=MapCompose(remove_whitespace), 
        output_processor=TakeFirst()  
    )
    ipa_br = scrapy.Field(
        input_processor=MapCompose(remove_whitespace), 
        output_processor=TakeFirst()
    )
    word_type = scrapy.Field(
        input_processor=MapCompose(), 
        output_processor=TakeFirst()
    )
    word_level = scrapy.Field(
        input_processor=MapCompose(get_word_level_from_url),
        output_processor=TakeFirst(),
    )
# fmt: on


class DefinitionItem(scrapy.Item):
    definition = scrapy.Field(input_processor=MapCompose(remove_tags))
    cefr = scrapy.Field(input_processor=MapCompose(get_word_level_from_url))
    grammar = scrapy.Field(input_processor=MapCompose(remove_tags))
    def_type = scrapy.Field(input_processor=MapCompose(remove_tags))
    context = scrapy.Field(input_processor=MapCompose(remove_tags))
    labels = scrapy.Field(input_processor=MapCompose(remove_tags))
    variants = scrapy.Field(input_processor=MapCompose(remove_tags))
    use = scrapy.Field(input_processor=MapCompose(remove_tags))
    synonyms = scrapy.Field(input_processor=MapCompose(remove_tags))
    examples = scrapy.Field(
        input_processor=Compose(join_examples),
        output_processor=MapCompose(remove_tags, listfy_examples),
    )
