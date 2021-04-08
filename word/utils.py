from enum import Enum

import factory

from word.model import dictionary


class CommandEnum(Enum):
    POST = 'post'
    SEARCH = 'search'
    DELETE = 'delete'


class DocFactory(factory.Factory):
    class Meta:
        model = dictionary.Dictionary

    word = factory.Sequence(lambda n: f'word-{n}')
    definitions = factory.Sequence(lambda n: f'definitions-{n}')
    syllables = factory.Sequence(lambda n: f'syllables-{n}')
    pronunciation = factory.Sequence(lambda n: f'pronunciation-{n}')
    rhyme_patterns = factory.Sequence(lambda n: f'rhyme_patterns-{n}')
    frequency = factory.Sequence(lambda n: f'frequency-{n}')
    letters = factory.Sequence(lambda n: f'letters-{n}')
    sounds = factory.Sequence(lambda n: f'sounds-{n}')
    examples = factory.List([factory.Sequence(lambda n : f'example-{n}') for _ in range(5)])
