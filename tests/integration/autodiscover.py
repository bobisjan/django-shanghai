from django.test import TestCase
from django.test.utils import override_settings

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


class AuthResourcesTestCase(TestCase):

    def test_app_should_have_auth_resources_by_default(self):
        self.assertIsNotNone(shanghai.api.resource_for('groups'))
        self.assertIsNotNone(shanghai.api.resource_for('users'))

    @override_settings(SHANGHAI_AUTH_RESOURCES=False)
    def test_app_should_not_have_auth_resources(self):
        api = shanghai.Shanghai()

        shanghai.discover(api)

        self.assertIsNone(api.resource_for('groups'))
        self.assertIsNone(api.resource_for('users'))
