


Dados que quero retirar:

word: str
word_cefr: str
word_type: str
ipa_nam: str
ipa_br: str

definitions: [ [.sense]
  {
    cefr: str
    grammar: str [.grammar]
    type: str [.pos]  # linking verb
    context: str [.cf]
    labels: str [.labels]
    definition: str [.def]
    variants: [.variants]
    use: [.use]
    synonyms: [.synonyms]
    examples: [
      {
        example: str [.x] ou [.unx]
        context: str [.cf]
        labels: str [.labels]
      }
    ]
  },
  ...
] 
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