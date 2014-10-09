from unittest import TestCase

import shanghai
from shanghai.apps import ShanghaiConfig


class ShanghaiTestCase(TestCase):

    def test_default_app_config(self):
        self.assertEqual(shanghai.default_app_config, 'shanghai.apps.ShanghaiConfig')

    def test_app_should_have_register_attribute(self):
        app = shanghai.Shanghai()
        self.assertTrue(hasattr(app, '_registry'))

        register = getattr(app, '_registry', None)
        self.assertTrue(type(register) is dict)

    def test_api_should_not_be_none(self):
        self.assertIsNotNone(shanghai.api)


class ShanghaiConfigTestCase(TestCase):

    def setUp(self):
        self.config = ShanghaiConfig('shanghai', shanghai)

    def test_name(self):
        self.assertEqual(self.config.name, 'shanghai')

    def test_verbose_name(self):
        self.assertEqual(self.config.verbose_name, 'Shanghai')
