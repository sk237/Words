import io
import unittest
from unittest import (
    mock,
    TestCase,
)

import elasticsearch
from elasticmock import (
    elasticmock,
    FakeElasticsearch,
)

from elasticsearch import NotFoundError

from word.service.search_service import SearchService


class SearchServiceTest(TestCase):

    @elasticmock
    def setUp(self):
        super().setUp()
        self.indices = ['key']
        self.body = {
            'key': 'value'
        }
        self.es = elasticsearch.Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
        self.search_service = SearchService(self.es)
        self.response = {
            'hits': {
                'hits': [
                    {
                        '_source': {'key': 'value'}
                    },
                ]
            }
        }

    def test_should_create_fake_es_instance(self):
        self.assertIsInstance(self.es, FakeElasticsearch)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_search_service_run_response(self, mock_stdout):
        self.es.index(index='key', body=self.body)
        self.search_service.run(key='key', value='value', size=1)
        self.search_service.print_response(res=self.response)
        self.assertEqual(mock_stdout.getvalue(), '-*-' * 30 + '\n' + '\nkey: value\n\n' + '-*-' * 30 + '\n')

    @unittest.mock.patch('elasticmock.fake_indices.FakeIndicesClient.exists')
    def test_should_raise_not_found_exception_when_search_not_exists_index(self, mocked_exists):
        mocked_exists.return_value(False)
        with self.assertRaises(NotFoundError):
            self.search_service.run(key='key', value='value', size=1)

    @unittest.mock.patch('elasticmock.fake_indices.FakeIndicesClient.exists')
    @unittest.mock.patch('elasticmock.FakeElasticsearch.search')
    def test_elasticsearch_search_is_called(self, mocked_exists, mocked_search):
        mocked_exists.return_value(True)
        self.search_service.run(key='key', value='value', size=1)
        mocked_search.assert_called_once()

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_echo_response(self, mock_stdout):
        self.search_service.print_response(res=self.response)
        self.assertEqual(mock_stdout.getvalue(), '-*-' * 30 + '\n' + '\nkey: value\n\n' + '-*-' * 30 + '\n')
