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

from word.utils import WordFactory, DocFactory, ExamplesFactory
from word.service.post_service import PostService


class PostServiceTest(TestCase):
    @elasticmock
    def setUp(self):
        super().setUp()
        self.indices = ['word', 'doc', 'examples']

        self.es = elasticsearch.Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
        self.post_service = PostService(self.es, self.indices)

    def test_should_create_fake_es_instance(self):
        self.assertIsInstance(self.es, FakeElasticsearch)

    @unittest.mock.patch('elasticmock.FakeElasticsearch.bulk')
    @unittest.mock.patch('word.service.post_service.PostService._draw_progress_bar')
    def test_post_to_elasticsearch_bulk_is_called_thrice(self, mocked_bulk, _):
        sample_dict = {
            'word': [WordFactory.create()],
            'doc': [DocFactory.create()],
            'examples': [ExamplesFactory.create()],
        }

        self.post_service.run(sample_dict)
        self.assertEqual(mocked_bulk.call_count, 3)

    @unittest.mock.patch('elasticmock.FakeElasticsearch.bulk')
    @unittest.mock.patch('word.service.post_service.PostService._draw_progress_bar')
    def test_post_to_elasticsearch_bulk_batch_once(self, mocked_bulk, _):
        sample_dict = {'examples': []}
        for i in range(499):
            sample_dict['examples'].append(ExamplesFactory.create())

        self.post_service.run(sample_dict)
        mocked_bulk.assert_called_once()

    @unittest.mock.patch('elasticmock.FakeElasticsearch.bulk')
    @unittest.mock.patch('word.service.post_service.PostService._draw_progress_bar')
    def test_post_to_elasticsearch_bulk_batch_twice(self, mocked_bulk, _):
        sample_dict = {'examples': []}
        for i in range(501):
            sample_dict['examples'].append(WordFactory.create())
        self.post_service.run(sample_dict)
        self.assertEqual(mocked_bulk.call_count, 2)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test__draw_progress_bar(self, mock_stdout):
        self.post_service._draw_progress_bar(1, 40)
        self.assertEqual(mock_stdout.getvalue(), '\r[========================================] 100%')
