from elasticsearch import (
    Elasticsearch,
    NotFoundError,
)


class DeleteService:

    def __init__(self, elastic_search: Elasticsearch, index: str):
        self.es = elastic_search
        self.index = index

    def run(self):
        self.es.indices.delete(self.index, ignore=[400, 404])
