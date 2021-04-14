from elasticsearch_dsl import (
    Document,
    Integer,
    Text,
)


class Dictionary(Document):
    word: Text()
    definitions: Text()
    syllables: Text()
    pronunciation: Text()
    rhyme_patterns: Text()
    frequency: Text()
    letters: Integer()
    sounds: Integer()
    examples: list[Text()]

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