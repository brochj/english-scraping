import scrapy

from scrapy.loader import ItemLoader
from oxford.items import OxfordItem


class DefinitionSpider(scrapy.Spider):
    name = "definition"
    allowed_domains = ["www.oxfordlearnersdictionaries.com"]
    start_urls = [
        "https://www.oxfordlearnersdictionaries.com/us/definition/english/umbrella",
        "https://www.oxfordlearnersdictionaries.com/us/definition/english/test",
        "https://www.oxfordlearnersdictionaries.com/us/definition/english/bus",
    ]

    def parse(self, response):
        self.logger.info("\n" * 5)

        # yield {"ipa_nam": response.css(".phons_n_am span::text").get()}

        loader = ItemLoader(item=OxfordItem(), selector=response)
        loader.add_css("ipa_nam", ".phons_n_am span.phon::text")
        loader.add_css("ipa_br", ".phons_br span::text")
        loader.add_css("word_type", ".webtop span.pos::text")
        loader.add_css("word_level", ".webtop div.symbols a::attr(href)")

        # loader = self.parse_definitions(response, loader)

        yield loader.load_item()

    def parse_definitions(self, res, loader):
        ol = res.css("ol.senses_multiple") or res.css("ol.sense_single")
        definitions = ol.css("span.shcut-g").getall()

        yield loader.load_item()
