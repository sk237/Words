import json

from elasticsearch import Elasticsearch

from word.model.dictionary import Dictionary
from word.service.delete_service import DeleteService
from word.service.post_service import PostService
from word.service.search_service import SearchService
from word.utils import CommandEnum


class CommandFactory:

    def __init__(self, host: str, port: str, index: str):
        self.es = Elasticsearch(host + port)
        self.index = index

    def mapper(self, command_enum: CommandEnum):
        if command_enum == CommandEnum.POST:
            return PostService(self.es, self.index)
        elif command_enum == CommandEnum.DELETE:
            return DeleteService(self.es, self.index)
        elif command_enum == CommandEnum.SEARCH:
            return SearchService(self.es, self.index)


class JsonParser:

    def parse_to_obj(self, file_path) -> list[Dictionary]:
        with open(file_path) as f:
            json_data = json.load(f)

        word_list: list[Dictionary] = []

        for word in json_data:
            dictionary = json_data[word]
            examples = []
            if 'definitions' in dictionary:
                for definition in dictionary['definitions']:
                    if 'examples' in definition:
                        examples.extend(definition.pop('examples'))

            word_list.append(
                Dictionary(
                    word,
                    examples=examples,
                    definitions=self._get_text(dictionary, 'definitions'),
                    syllables=self._get_text(dictionary, 'syllables'),
                    pronunciation=self._get_text(dictionary, 'pronunciation'),
                    rhyme_patterns=self._get_text(dictionary, 'rhymePatterns'),
                    frequency=self._get_text(dictionary, 'frequency'),
                    letters=dictionary.get('letters', None),
                    sounds=dictionary.get('sounds', None),
                    )
            )

        return word_list

    @staticmethod
    def _get_text(description_map, key):
        if key not in description_map:
            return None
        return str(description_map.get(key))
