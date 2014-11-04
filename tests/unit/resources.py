from django.test import TestCase

from shanghai.apps import Shanghai
from shanghai.serializers import Serializer

from tests.fixtures.resources import ArticleResource, CategoryResource


class BaseResourceTestCase(TestCase):

    def setUp(self):
        self.api = Shanghai()

    def test_resource_should_have_name_from_class_property(self):
        resource = CategoryResource(self.api)
        self.assertEqual(resource.name, 'categories')

    def test_resource_should_have_name_from_class_name(self):
        resource = ArticleResource(self.api)
        self.assertEqual(resource.name, 'articles')

    def test_resource_should_have_serializer(self):
        resource = ArticleResource(self.api)
        self.assertIsNotNone(resource.serializer)
        self.assertTrue(isinstance(resource.serializer, Serializer))
