import sys

from elasticsearch import (
    Elasticsearch,
    helpers,
)

from word.model.dictionary import Dictionary


class PostService:

    def __init__(self, elastic_search: Elasticsearch, index: str):
        self.es = elastic_search
        self.index = index
        self.batch = 500

    def run(self, word_list: list[Dictionary]):
        progress = 0
        word_list_size = len(word_list)

        bulk_list = []

        Dictionary.init(index=self.index, using=self.es)

        for sample in word_list:
            bulk_list.append({
                '_index': self.index,
                '_source': sample.to_dict(),
            })
            progress += 1

            if len(bulk_list) % self.batch == 0:
                helpers.bulk(self.es, bulk_list)
                bulk_list.clear()
                self._draw_progress_bar(progress / word_list_size, 40)

        helpers.bulk(self.es, bulk_list)
        self._draw_progress_bar(progress / word_list_size, 40)

    @staticmethod
    def _draw_progress_bar(percent, bar_len):
        # percent float from 0 to 1.
        sys.stdout.write("\r")
        sys.stdout.write("[{:<{}}] {:.0f}%".format("=" * int(bar_len * percent), bar_len, percent * 100))
        sys.stdout.flush()
