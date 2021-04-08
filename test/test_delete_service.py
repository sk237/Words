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

from word.service.delete_service import DeleteService


class DeleteServiceTest(TestCase):

    @elasticmock
    def setUp(self):
        super().setUp()
        self.index = 'test-index_1'
        self.body = {
            'key': 'value'
        }

        self.es = elasticsearch.Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
        self.delete_service = DeleteService(self.es, self.index)

    def test_should_create_fake_es_instance(self):
        self.assertIsInstance(self.es, FakeElasticsearch)

    @unittest.mock.patch('elasticmock.fake_indices.FakeIndicesClient.delete')
    def test_elasticsearch_delete_is_called_thrice(self, mocked_indices_delete):
        self.delete_service.run()
        self.assertEqual(mocked_indices_delete.call_count, 1)

    def test_search_index_should_raise_not_found_error(self):
        self.es.index(index=self.index, body=self.body)
        search = self.es.search(index=self.index)

        self.delete_service.run()

        self.assertEqual(1, search.get('hits').get('total').get('value'))
        with self.assertRaises(NotFoundError):
            self.es.search(index=self.index)
