import scrapy

from scrapy.loader import ItemLoader
from oxford.items import OxfordItem, DefinitionItem
from w3lib.html import remove_tags


class DefinitionSpider(scrapy.Spider):
    name = "definition"
    allowed_domains = ["www.oxfordlearnersdictionaries.com"]
    # start_urls = [
    #     "https://www.oxfordlearnersdictionaries.com/us/definition/english/cable",
    #     "https://www.oxfordlearnersdictionaries.com/us/definition/english/test",
    #     "https://www.oxfordlearnersdictionaries.com/us/definition/english/get",
    #     "https://www.oxfordlearnersdictionaries.com/us/definition/english/veranda",
    #     "https://www.oxfordlearnersdictionaries.com/us/definition/english/should",
    # ]

    base_url = "https://www.oxfordlearnersdictionaries.com/us/definition/english/"
    words_list_file = "test"

    def read_words_list(self):
        with open(f"{self.words_list_file}.txt") as file:
            return [line.rstrip() for line in file]

    def start_requests(self):
        words = self.read_words_list()
        urls = [self.base_url + word for word in words]

        for url in urls:
            word = url.split("/")[-1]
            yield scrapy.Request(url, self.parse, errback=self.handle_error)

    def parse(self, response):
        loader = ItemLoader(item=OxfordItem(), selector=response)

        loader.add_css("word", "h1.headword::text")
        loader.add_css("ipa_nam", ".phons_n_am span.phon::text")
        loader.add_css("ipa_br", ".phons_br span::text")
        loader.add_css("word_type", ".webtop span.pos::text")
        loader.add_css("cefr", ".webtop div.symbols a::attr(href)")

        item = loader.load_item()

        def_loader = ItemLoader(item=DefinitionItem(), selector=response)

        # def_li = def_loader.nested_css(".top-container + ol li")
        # def_li.add_css("definition", "span.def")
        # def_li.add_css("cefr", ".symbols a::attr(href)")

        for def_li in response.css(".top-container + ol")[0].css("li.sense"):
            definition = def_li.css("span.def").get()
            cefr = def_li.css(".symbols a::attr(href)").get() or ""
            grammar = def_li.css(".grammar").get() or ""
            def_type = def_li.css(".pos").get() or ""
            context = def_li.css(".cf").get() or ""
            labels = def_li.css(".labels").get() or ""
            variants = def_li.css(".variants").get() or ""
            use = def_li.css(".use").get() or ""
            synonyms = def_li.css(".synonyms").get() or ""

            examples = def_li.css("span.x").getall()

            def_loader.add_value("definition", definition)
            def_loader.add_value("cefr", cefr)
            def_loader.add_value("grammar", grammar)
            def_loader.add_value("def_type", def_type)
            def_loader.add_value("context", context)
            def_loader.add_value("labels", labels)
            def_loader.add_value("variants", variants)
            def_loader.add_value("use", use)
            def_loader.add_value("synonyms", synonyms)
            def_loader.add_value("examples", examples)

        def_item = def_loader.load_item()

        # self.printer("before return item")
        # # self.logger.info(item, def_item)
        # self.logger.info(item)
        # self.logger.info(response.request.url)
        # self.printer("end return item")
        return item  # , def_item

    def handle_error(self, failure):
        url = failure.request.url
        self.logger.error("Failure type: %s, URL: %s", failure.type, url)

    def printer(self, value: str = "aqui"):
        self.logger.info("-" * 50)
        self.logger.info(value.center(50))
        self.logger.info("-" * 50)
