from django.test import TestCase

from shanghai.utils import is_iterable


class IsIterableTestCase(TestCase):

    def test_list(self):
        self.assertTrue(is_iterable([]))

    def test_object(self):
        self.assertFalse(is_iterable(object()))

    def test_none(self):
        self.assertFalse(is_iterable(None))
