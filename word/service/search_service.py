from elasticsearch import (
    Elasticsearch,
    NotFoundError,
)


class SearchService:

    def __init__(self, elastic_search: Elasticsearch, index):
        self.es = elastic_search
        self.index = index

    def run(self, key: str, value: str, size: int):
        if not self.es.indices.exists(index=self.index):
            raise NotFoundError("Post sample words before search")

        doc = {
            "size": size,
            "query": {
                "match": {
                    key: {
                        "query": value,
                        "fuzziness": "auto",
                        'fuzzy_transpositions': True,
                    }
                }
            }
        }
        res = self.es.search(body=doc, index=self.index)
        self._print_response(res)

    @staticmethod
    def _print_response(res):
        for hit in res['hits']['hits']:
            source = hit['_source']
            print('-*-' * 30)
            print('%s: %s' % ('word', source['word']))
            for source_key in source:
                if source_key == 'word':
                    continue
                source_value = source[source_key]
                print()
                print('%s: %s' % (source_key, source_value))
            print()
            print('-*-' * 30)
