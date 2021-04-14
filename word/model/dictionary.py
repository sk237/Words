from elasticsearch_dsl import (
    analyzer,
    Document,
    Integer,
    Text,
)


folding_analyzer = analyzer(
    'folding_analyzer',
    tokenizer="standard",
    filter=["lowercase", "asciifolding"]
)


class Dictionary(Document):
    word: Text(analyzer=folding_analyzer)
    definitions: Text()
    syllables: Text()
    pronunciation: Text()
    rhyme_patterns: Text()
    frequency: Text()
    letters: Integer()
    sounds: Integer()
    examples: list[Text(analyzer=folding_analyzer)]

    class Index:
        name = 'dictionary'

    def __init__(
            self,
            word: Text(),
            examples: list[Text()],
            *,
            definitions: Text(),
            syllables: Text(),
            pronunciation: Text(),
            rhyme_patterns: Text(),
            frequency: Text(),
            letters: Integer(),
            sounds: Integer(),
    ):
        super().__init__()
        self.examples = examples
        self.word = word
        self.definitions = definitions
        self.syllables = syllables
        self.pronunciation = pronunciation
        self.rhyme_patterns = rhyme_patterns
        self.frequency = frequency
        self.letters = letters
        self.sounds = sounds
