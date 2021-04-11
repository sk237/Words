import json
import sys

from elasticsearch import (
    Elasticsearch,
    helpers,
)


from word.model.doc import Doc
from word.model.examples import Examples
from word.model.sample_word import SampleWord
from word.model.word import Word


class PostService:

    def __init__(self, elastic_search: Elasticsearch, indices: list[str]):
        self.es = elastic_search
        self.indices = indices
        self.batch = 1000

    def run(self, file_path):
        with open(file_path) as f:
            json_data = json.load(f)

        sample_dict: dict[str, list[SampleWord]] = {index: [] for index in self.indices}
        self.parse_json(json_data, sample_dict)

        bulk_dict: dict[str, []] = {index: [] for index in self.indices}
        self.post_to_elasticsearch(bulk_dict, sample_dict)

    def post_to_elasticsearch(self, bulk_dict, sample_dict):
        progress = 0
        word_list_size = len(sample_dict['word']) * 3

        for index in sample_dict:
            for sample in sample_dict[index]:
                bulk_dict[index].append({
                    '_index': index,
                    '_source': sample.__dict__,
                })
                progress += 1

                if progress % self.batch == 0:
                    for key in bulk_dict:
                        helpers.bulk(self.es, bulk_dict[key])
                        bulk_dict[key].clear()
                    self._draw_progress_bar(progress / word_list_size, 20)

            helpers.bulk(self.es, bulk_dict[index])
            self._draw_progress_bar(progress / word_list_size, 20)

    @staticmethod
    def parse_json(doc_data, sample_dict):
        for word in doc_data:
            dictionary = doc_data[word]
            examples = []
            if 'definitions' in dictionary:
                for definition in dictionary['definitions']:
                    if 'examples' in definition:
                        examples.extend(definition.pop('examples'))
            sample_dict['word'].append(Word(word))
            sample_dict['doc'].append(Doc(word, str(dictionary)))
            sample_dict['examples'].append(Examples(examples))

    @staticmethod
    def _draw_progress_bar(percent, bar_len):
        # percent float from 0 to 1.
        sys.stdout.write("\r")
        sys.stdout.write("[{:<{}}] {:.0f}%".format("=" * int(bar_len * percent), bar_len, percent * 100))
        sys.stdout.flush()
