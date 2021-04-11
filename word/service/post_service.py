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
        self.batch = 500

    def run(self, sample_dict):
        progress = 0
        word_list_size = 0
        word_list_size += sum(len(sample_dict[sample]) for sample in sample_dict)

        bulk_dict: dict[str, []] = {index: [] for index in self.indices}

        for index in sample_dict:
            for sample in sample_dict[index]:
                bulk_dict.get(index).append({
                    '_index': index,
                    '_source': sample.__dict__,
                })
                progress += 1

                if progress % self.batch == 0:
                    helpers.bulk(self.es, bulk_dict.get(index))
                    bulk_dict.get(index).clear()
                    self._draw_progress_bar(progress / word_list_size, 40)

            helpers.bulk(self.es, bulk_dict.get(index))
            self._draw_progress_bar(progress / word_list_size, 40)



    @staticmethod
    def _draw_progress_bar(percent, bar_len):
        # percent float from 0 to 1.
        sys.stdout.write("\r")
        sys.stdout.write("[{:<{}}] {:.0f}%".format("=" * int(bar_len * percent), bar_len, percent * 100))
        sys.stdout.flush()
