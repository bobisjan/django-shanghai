from django.test import TestCase

import shanghai
from shanghai.resources import ModelResource


class AutodiscoverTestCase(TestCase):

    def setUp(self):
        self.api = shanghai.api

    def test_app_should_have_registered_resources(self):
        articles = self.api.resource_for('articles')
        categories = self.api.resource_for('categories')

        self.assertIsNotNone(articles)
        self.assertIsNotNone(categories)

        self.assertTrue(isinstance(articles, ModelResource))
        self.assertTrue(isinstance(categories, ModelResource))
