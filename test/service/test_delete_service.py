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
        self.indices = ['test-index_1', 'test-index_2']
        self.body = {
            'key': 'value'
        }

        self.es = elasticsearch.Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
        self.delete_service = DeleteService(self.es, self.indices)

    def test_should_create_fake_es_instance(self):
        self.assertIsInstance(self.es, FakeElasticsearch)

    @unittest.mock.patch('elasticmock.fake_indices.FakeIndicesClient.delete')
    def test_elasticsearch_delete_is_called_thrice(self, mocked_delete):
        self.delete_service.run()
        self.assertEqual(mocked_delete.call_count, len(self.indices))

    def test_delete_indices_should_raise_not_found_error(self):
        for index in self.indices:
            self.es.index(index=index, body=self.body)

        for index in self.indices:
            search = self.es.search(index=index)
            self.assertEqual(1, search.get('hits').get('total').get('value'))

        self.delete_service.run()

        for index in self.indices:
            with self.assertRaises(NotFoundError):
                self.es.search(index=index)
