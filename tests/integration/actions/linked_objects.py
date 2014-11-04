from tests.test_cases import TestCase


class DeleteLinkedObjectsTestCase(TestCase):

    def test_app_should_remove_articles_from_category(self):
        response = self.client.delete('/api/categories/1/links/articles/1,3')

        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/articles/1/links/category')
        categories = response.document.get('categories')
        self.assertIsNone(categories)

        response = self.client.get('/api/articles/3/links/category')
        categories = response.document.get('categories')
        self.assertIsNone(categories)

    def test_app_should_respond_not_found_on_delete_belongs_to(self):
        response = self.client.delete('/api/articles/1/links/category/5,6')

        self.assertEqual(response.status_code, 404)
