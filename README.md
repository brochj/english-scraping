# Scraping English Words

## TODO's

- [x] - Adicionar Metódo para salvar palavras que receberam 404



```python
class WordItem(scrapy.Item):  
    word = scrapy.Field()
    ipa_nam = scrapy.Field()
    ipa_br = scrapy.Field()
    word_type = scrapy.Field()
    cefr = scrapy.Field()
    definitions = scrapy.Field() # [DefinitionItem, DefinitionItem]


class DefinitionItem(scrapy.Item):
    definition = scrapy.Field()
    cefr = scrapy.Field()
    grammar = scrapy.Field()
    def_type = scrapy.Field()
    context = scrapy.Field()
    labels = scrapy.Field()
    variants = scrapy.Field()
    use = scrapy.Field()
    synonyms = scrapy.Field()
    word_id = scrapy.Field()
    examples = scrapy.Field() # [ExampleItem, ExampleItem]


class ExampleItem(scrapy.Item):
    example = scrapy.Field()
    context = scrapy.Field()
    labels = scrapy.Field()
    definition_id = scrapy.Field()

```