from enum import Enum

import factory

from word.model import (
    doc,
    examples,
    word,
)


class CommandEnum(Enum):
    POST = 'post'
    SEARCH = 'search'
    DELETE = 'delete'


class WordFactory(factory.Factory):
    class Meta:
        model = word.Word

    word = factory.Sequence(lambda n: f'word-{n}')


class DocFactory(factory.Factory):
    class Meta:
        model = doc.Doc

    doc = factory.Sequence(lambda n: f'doc-{n}')
    dictionary = factory.Sequence(lambda n: f'dictionary-{n}')


class ExamplesFactory(factory.Factory):
    class Meta:
        model = examples.Examples

    examples = factory.Sequence(lambda n: f'examples-{n}')
