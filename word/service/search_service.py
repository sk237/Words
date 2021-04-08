import pprint

import click
import yaml
from elasticsearch import Elasticsearch


class SearchService:

    def __init__(self, elastic_search: Elasticsearch, index):
        self.es = elastic_search
        self.index = index

    def run(self, key: str, word: str, size: int):
        if not self.es.indices.exists(index=self.index):
            click.echo()
            click.echo("NotFoundError: Post sample words before search")
            return

        doc = {
            "size": size,
            "query": {
                "match": {
                    key: {
                        "query": word,
                        "fuzziness": 'auto',
                    }
                }
            }
        }
        res = self.es.search(body=doc, index=self.index)
        for hit in res['hits']['hits']:
            source = hit['_source']
            click.echo('-*-' * 30)
            click.echo('key word: ', source['key'])
            if source['examples']:
                click.echo('examples: ', source['examples'])
            click.echo()
            pprint.pprint(yaml.load(source['description'], yaml.Loader))
            click.echo('-*-' * 30)
