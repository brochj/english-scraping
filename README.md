


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