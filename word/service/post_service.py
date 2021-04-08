import json
import sys

from elasticsearch import (
    Elasticsearch,
    helpers,
)


from word.model.word import Word


class PostService:

    def __init__(self, elastic_search: Elasticsearch, index: str):
        self.es = elastic_search
        self.index = index
        self.batch = 1000

    def run(self, file_path):
        with open(file_path) as f:
            words_data = json.load(f)
        word_list = []
        for key in words_data:
            description = words_data[key]
            examples = []
            if 'definitions' in description:
                for definition in description['definitions']:
                    if 'examples' in definition:
                        examples.extend(definition.pop('examples'))

            word_list.append(Word(key, str(description), examples))

        bulk = []
        word_list_size = len(word_list)

        for i, word in enumerate(word_list):
            bulk.append({
                '_index': self.index,
                '_source': word.__dict__,
            })

            if i % self.batch == 0:
                helpers.bulk(self.es, bulk)
                bulk.clear()
                self._drawProgressBar(i / word_list_size, 20)

        helpers.bulk(self.es, bulk)
        self._drawProgressBar(1, 20)

    @staticmethod
    def _drawProgressBar(percent, barLen):
        # percent float from 0 to 1.
        sys.stdout.write("\r")
        sys.stdout.write("[{:<{}}] {:.0f}%".format("=" * int(barLen * percent), barLen, percent * 100))
        sys.stdout.flush()
