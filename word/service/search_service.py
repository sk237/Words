
from elasticsearch import (
    Elasticsearch,
    NotFoundError,
)


class SearchService:

    def __init__(self, elastic_search: Elasticsearch):
        self.es = elastic_search

    def run(self, key: str, value: str, size: int):
        if not self.es.indices.exists(index=key):
            raise NotFoundError("Post sample words before search")

        doc = {
            "size": size,
            "query": {
                "match": {
                    key: {
                        "query": value,
                        "fuzziness": 'auto',
                    }
                }
            }
        }
        res = self.es.search(body=doc, index=key)

        self.print_response(res)

    @staticmethod
    def print_response(res):
        for hit in res['hits']['hits']:
            source = hit['_source']
            print('-*-' * 30)
            for source_key in source:
                source_value = source[source_key]
                print()
                print('%s: %s' % (source_key, source_value))
            print()
            print('-*-' * 30)
