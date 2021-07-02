# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def remove_whitespace(text):
    return text.strip()


def get_word_level_from_url(url):
    return url[-2:]


class OxfordItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ipa_nam = scrapy.Field(
        input_processor=MapCompose(remove_whitespace), output_processor=TakeFirst()
    )
    ipa_br = scrapy.Field(
        input_processor=MapCompose(remove_whitespace), output_processor=TakeFirst()
    )
    word_type = scrapy.Field(input_processor=MapCompose(), output_processor=TakeFirst())
    word_level = scrapy.Field(
        input_processor=MapCompose(get_word_level_from_url),
        output_processor=TakeFirst(),
    )
    definitions = scrapy.Field(
        input_processor=MapCompose(), output_processor=TakeFirst()
    )
