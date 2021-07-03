import scrapy

from scrapy.loader import ItemLoader
from oxford.items import OxfordItem, DefinitionItem
from w3lib.html import remove_tags


class DefinitionSpider(scrapy.Spider):
    name = "definition"
    allowed_domains = ["www.oxfordlearnersdictionaries.com"]
    start_urls = [
        "https://www.oxfordlearnersdictionaries.com/us/definition/english/cable",
        "https://www.oxfordlearnersdictionaries.com/us/definition/english/test",
        "https://www.oxfordlearnersdictionaries.com/us/definition/english/car",
        "https://www.oxfordlearnersdictionaries.com/us/definition/english/get",
        # "https://www.oxfordlearnersdictionaries.com/us/definition/english/should",
    ]

    def printer(self, value: str = "aqui"):
        self.logger.info("-" * 50)
        self.logger.info(value.center(50))
        self.logger.info("-" * 50)

    def parse(self, response):
        loader = ItemLoader(item=OxfordItem(), selector=response)

        loader.add_css("ipa_nam", ".phons_n_am span.phon::text")
        loader.add_css("ipa_br", ".phons_br span::text")
        loader.add_css("word_type", ".webtop span.pos::text")
        loader.add_css("word_level", ".webtop div.symbols a::attr(href)")

        item = loader.load_item()

        def_loader = ItemLoader(item=DefinitionItem(), selector=response)

        # def_li = def_loader.nested_css(".top-container + ol li")
        # def_li.add_css("definition", "span.def")
        # def_li.add_css("cefr", ".symbols a::attr(href)")

        # for def_li in response.css(".top-container + ol li"):
        for def_li in response.css(".top-container + ol")[0].css("li.sense"):
            definition = def_li.css("span.def").get()
            cefr = def_li.css(".symbols a::attr(href)").get() or ""
            def_loader.add_value("definition", definition)
            def_loader.add_value("cefr", cefr)

        def_item = def_loader.load_item()

        self.printer("before return item")
        self.logger.info(item, def_item)
        self.printer("end return item")
        return item, def_item
