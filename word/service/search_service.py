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

        doc = self._build_best_search_template(size, key, value)
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

    @staticmethod
    def _build_best_search_template(size, key, value) -> dict:
        return {
            "size": size,
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                key: {
                                    "query": value,
                                    "fuzziness": "auto",
                                    'fuzzy_transpositions': True,
                                    "prefix_length": 1,
                                }
                            }
                        },
                        {
                            "match": {
                                key: {
                                    "query": value,
                                    "fuzziness": "auto",
                                    'fuzzy_transpositions': True,
                                    "prefix_length": 1,
                                    "operator": "and"
                                }
                            }
                        },
                        {
                            "match_phrase": {
                                key: {
                                    "query": value,
                                    "boost": 2
                                }
                            }
                        }
                    ]
                }
            }
        }

    @staticmethod
    def _build_performance_template(size, key, value) -> dict:
        return {
            "size": size,
            "query": {
                "match": {
                    key: {
                        "query": value,
                        "fuzziness": "auto",
                        'fuzzy_transpositions': True,
                        "prefix_length": 1,
                    }
                }
            }
        }
