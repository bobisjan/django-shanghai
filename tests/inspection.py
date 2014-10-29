from unittest import TestCase

from shanghai.apps import Shanghai

from tests.fixtures.resources import ArticleResource, CategoryResource


class InspectorTestCase(TestCase):

    def __init__(self, methodName='runTest'):
        super(InspectorTestCase, self).__init__(methodName=methodName)
        self.api = None
        self.article = None
        self.category = None

    def setUp(self):
        self.api = Shanghai()
        self.api.register(ArticleResource)
        self.api.register(CategoryResource)

        self.article = self.api.resource_for('articles')
        self.category = self.api.resource_for('categories')

        self.api.inspect()

    def test_resource_should_have_id(self):
        self.assertIsNotNone(self.article.get_id())
        self.assertIsNotNone(self.category.get_id())

    def test_resource_should_have_attributes(self):
        self.assertTrue('title' in self.article.get_attributes())
        self.assertTrue('perex' in self.article.get_attributes())
        self.assertTrue('title' in self.category.get_attributes())

    def test_resource_should_have_relationships(self):
        self.assertTrue('category' in self.article.get_relationships())
        self.assertTrue('articles' in self.category.get_relationships())


class ModelInspectorTestCase(TestCase):

    def __init__(self, methodName='runTest'):
        super(ModelInspectorTestCase, self).__init__(methodName=methodName)
        self.api = None
        self.article = None
        self.category = None

    def setUp(self):
        self.api = Shanghai()
        self.api.register(ArticleResource)
        self.api.register(CategoryResource)

        self.article = self.api.resource_for('articles')
        self.category = self.api.resource_for('categories')

        self.api.inspect()

    def test_resource_should_have_id(self):
        self.assertIsNotNone(self.article.get_id())
        self.assertIsNotNone(self.category.get_id())

    def test_resource_should_have_attributes(self):
        self.assertTrue('title' in self.article.get_attributes())
        self.assertTrue('perex' in self.article.get_attributes())
        self.assertTrue('title' in self.category.get_attributes())

    def test_resource_should_have_relationships(self):
        self.assertTrue('category' in self.article.get_relationships())
        self.assertTrue('articles' in self.category.get_relationships())