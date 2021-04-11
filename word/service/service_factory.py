from elasticsearch import Elasticsearch

from word.model.service_enum import CommandEnum
from word.service.delete_service import DeleteService
from word.service.post_service import PostService
from word.service.search_service import SearchService


class ServiceFactory:

    def __init__(self, host: str, port: str, indices: list[str]):
        self.es = Elasticsearch(host + port)
        self.indices = indices

    def mapper(self, command_enum: CommandEnum):
        if command_enum == CommandEnum.POST:
            return PostService(self.es, self.indices)
        elif command_enum == CommandEnum.DELETE:
            return DeleteService(self.es, self.indices)
        elif command_enum == CommandEnum.SEARCH:
            return SearchService(self.es)
