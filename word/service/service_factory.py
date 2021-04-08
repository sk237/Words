from elasticsearch import Elasticsearch

from word.model.service_enum import Command
from word.service.delete_service import DeleteService
from word.service.post_service import PostService
from word.service.search_service import SearchService


class ServiceFactory:

    def __init__(self, host: str, port: str, index: str):
        self.es = Elasticsearch(host + port)
        self.index = index

    def mapper(self, command: Command):
        if command == Command.POST:
            return PostService(self.es, self.index)
        elif command == Command.DELETE:
            return DeleteService(self.es, self.index)
        elif command == Command.SEARCH:
            return SearchService(self.es, self.index)
