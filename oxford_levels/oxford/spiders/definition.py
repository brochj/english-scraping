import scrapy

from scrapy.loader import ItemLoader
from itemloaders import ItemAdapter
from oxford.items import WordItem, DefinitionItem, ExampleItem
from oxford.items import rm_tags, get_cefr_from_url
from copy import deepcopy
import json
import ast


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
    words_list_file = "s123_w123"

    def read_dict_line_from_txt(self) -> list:
        with open(f"{self.words_list_file}.txt", "r") as file:
            return [ast.literal_eval(line.rstrip()) for line in file]

    def start_requests(self):
        words = self.read_dict_line_from_txt()

        for data in words:
            url = self.base_url + data.get("word")
            yield scrapy.Request(
                url, self.parse, errback=self.handle_error, cb_kwargs=data
            )

    def parse(self, response, word, speaking, writing, word_type):
        def_dict = {
            "definition": "",
            "cefr": "",
            "grammar": "",
            "def_type": "",
            "context": "",
            "labels": "",
            "variants": "",
            "use": "",
            "synonyms": "",
            "examples": [],
        }
        ex_dict = {
            "example": "",
            "context": "",
            "labels": "",
        }

        loader = ItemLoader(item=WordItem(), selector=response)

        loader.add_css("word", "h1.headword::text")
        loader.add_css("ipa_nam", ".phons_n_am span.phon::text")
        loader.add_css("ipa_br", ".phons_br span::text")
        loader.add_css("word_type", ".webtop span.pos::text")
        loader.add_css("cefr", ".webtop div.symbols a::attr(href)")
        loader.add_value("speaking", speaking)
        loader.add_value("writing", writing)

        definitions = response.css(".top-container + ol")[0].css("li.sense")
        defs = []
        for def_li in definitions:

            def_dict["definition"] = def_li.css("span.def").get() or ""
            def_dict["cefr"] = def_li.css(".symbols a::attr(href)").get() or ""
            def_dict["grammar"] = def_li.css(".grammar").get() or ""
            def_dict["def_type"] = def_li.css(".pos").get() or ""
            def_dict["context"] = def_li.css(".cf").get() or ""
            def_dict["labels"] = def_li.css(".labels").get() or ""
            def_dict["variants"] = def_li.css(".variants").get() or ""
            def_dict["use"] = def_li.css(".use").get() or ""
            def_dict["synonyms"] = def_li.css(".synonyms").get() or ""

            def_dict["cefr"] = get_cefr_from_url(def_dict["cefr"])

            def_dict["examples"] = []
            for example in def_li.css("li > ul.examples > li"):
                example_dict = {}
                example_dict["example"] = example.css("span.x").get() or ""
                example_dict["context"] = example.css("span.cf").get() or ""
                example_dict["labels"] = example.css("span.labels").get() or ""

                if not example_dict["example"] == "":
                    def_dict["examples"].append(rm_tags(example_dict))

            defs.append(rm_tags(def_dict))

        loader.add_value("definitions", defs)

        item = loader.load_item()
        return item

    def handle_error(self, failure):
        url = failure.request.url
        self.save_to_txt(url, "url_failures")
        self.logger.error("Failure type: %s, URL: %s", failure.type, url)
        # if you want to try more endpoints with the word that occured error
        # uncomment the next lines
        # Attention: For each Error, it will try more 20 endpoints
        # so, it will take some time
        # Run first without it, then create a word list containing only the words
        # that generate error
        ENDPOINTS = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "_1",
            "_2",
            "_3",
            "_4",
            "_5",
            "1_1",
            "1_2",
            "1_3",
            "1_4",
            "1_5",
            "2_1",
            "2_2",
            "2_3",
            "2_4",
            "2_5",
        ]

        for endpoint in ENDPOINTS:
            yield scrapy.Request(
                url=f"{url}{endpoint}".lower(),
                callback=self.parse,
                cb_kwargs=failure.request.cb_kwargs,
            )

    def save_to_txt(self, value, filename: str) -> None:
        with open(filename + ".txt", "a", encoding="utf-8") as file:
            file.write(str(value) + "\n")

    def printer(self, value: str = "aqui"):
        self.logger.info("-" * 50)
        self.logger.info(value.center(50))
        self.logger.info("-" * 50)
