from elasticsearch import Elasticsearch


class DeleteService:

    def __init__(self, elastic_search: Elasticsearch, indices: list[str]):
        self.es = elastic_search
        self.indices = indices

    def run(self):
        for index in self.indices:
            self.es.indices.delete(index, ignore=[400, 404])
