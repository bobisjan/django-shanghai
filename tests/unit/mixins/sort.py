from django.test import TestCase, RequestFactory

from shanghai.mixins.sort import ModelSortMixin


class SortTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.mixin = ModelSortMixin()

    def test_sort_parameters(self):
        self.mixin.request = self.factory.get('api/articles?sort=%2Btitle,-category.name')

        params = self.mixin.sort_parameters()

        self.assertEqual(params[0], 'title')
        self.assertEqual(params[1], '-category__name')
