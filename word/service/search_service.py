import pprint

import click
from elasticsearch import Elasticsearch


class SearchService:

    def __init__(self, elastic_search: Elasticsearch):
        self.es = elastic_search

    def run(self, key: str, value: str, size: int):
        if not self.es.indices.exists(index=key):
            print()
            print("NotFoundError: Post sample words before search")
            return

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
            click.echo('-*-' * 30)
            for source_key in source:
                source_value = source[source_key]
                pprint.pprint('%s: %s' % (source_key, source_value))
                click.echo()
            click.echo('-*-' * 30)
