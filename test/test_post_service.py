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

from word.utils import DocFactory
from word.service.post_service import PostService


class PostServiceTest(TestCase):
    @elasticmock
    def setUp(self):
        super().setUp()
        self.index = 'dictionary'

        self.es = elasticsearch.Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
        self.post_service = PostService(self.es, self.index)

    def test_should_create_fake_es_instance(self):
        self.assertIsInstance(self.es, FakeElasticsearch)

    @unittest.mock.patch('elasticmock.FakeElasticsearch.bulk')
    @unittest.mock.patch('word.service.post_service.PostService._draw_progress_bar')
    def test_post_to_elasticsearch_bulk_is_called_thrice(self, mocked_bulk, _):
        word_list = [DocFactory.create(), DocFactory.create(), DocFactory.create()]

        self.post_service.run(word_list)
        self.assertEqual(mocked_bulk.call_count, 1)

    @unittest.mock.patch('elasticmock.FakeElasticsearch.bulk')
    @unittest.mock.patch('word.service.post_service.PostService._draw_progress_bar')
    def test_post_to_elasticsearch_bulk_batch_once(self, mocked_bulk, _):
        word_list = []
        for i in range(499):
            word_list.append(DocFactory.create())

        self.post_service.run(word_list)
        mocked_bulk.assert_called_once()

    @unittest.mock.patch('elasticmock.FakeElasticsearch.bulk')
    @unittest.mock.patch('word.service.post_service.PostService._draw_progress_bar')
    def test_post_to_elasticsearch_bulk_batch_twice(self, mocked_bulk, _):
        word_list = []
        for i in range(501):
            word_list.append(DocFactory.create())
        self.post_service.run(word_list)
        self.assertEqual(mocked_bulk.call_count, 2)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__draw_progress_bar(self, mock_stdout):
        self.post_service._draw_progress_bar(1, 40)
        self.assertEqual(mock_stdout.getvalue(), '\r[========================================] 100%')
