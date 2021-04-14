import json

from elasticsearch import Elasticsearch

from word.model.doc import Doc
from word.model.examples import Examples
from word.model.sample_word import SampleWord
from word.model.word import Word
from word.service.delete_service import DeleteService
from word.service.post_service import PostService
from word.service.search_service import SearchService
from word.utils import CommandEnum


class CommandFactory:

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


class JsonParser:

    def __init__(self, indices: list[str]):
        self.indices = indices

    def parse_to_dic(self, file_path) -> dict[str, list[SampleWord]]:
        with open(file_path) as f:
            json_data = json.load(f)

        sample_dict: dict[str, list[SampleWord]] = {index: [] for index in self.indices}

        for keyword in json_data:
            dictionary = json_data[keyword]
            keyword_examples = []
            if 'definitions' in dictionary:
                for definition in dictionary['definitions']:
                    if 'examples' in definition:
                        keyword_examples.extend(definition.pop('examples'))
            sample_dict['word'].append(Word(keyword))
            sample_dict['doc'].append(Doc(keyword, str(dictionary)))
            sample_dict['examples'].append(Examples(keyword_examples))

        return sample_dict

