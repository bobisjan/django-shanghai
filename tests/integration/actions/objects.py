from tests.test_cases import TestCase


class GetObjectsTestCase(TestCase):

    def test_app_should_respond_with_articles(self):
        response = self.client.get('/api/articles/1,2')

        self.assertEqual(response.status_code, 200)

        articles = response.document.get('articles', None)

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        self.assertEqual(len(articles), 2)


class GetEmptyObjectsTestCase(TestCase):

    fixtures = None

    def test_app_should_return_empty_array(self):
        response = self.client.get('/api/articles/26,32')

        self.assertEqual(response.status_code, 404)


class DeleteObjectsTestCase(TestCase):

    def test_app_should_delete_articles(self):
        response = self.client.delete('/api/articles/1,3')
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/articles/1,3')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/api/articles/1')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/api/articles/3')
        self.assertEqual(response.status_code, 404)

    def test_app_should_respond_with_not_found_for_non_existing_articles(self):
        response = self.client.delete('/api/articles/105,106')
        self.assertEqual(response.status_code, 404)

        response = self.client.delete('/api/articles/1,106')
        self.assertEqual(response.status_code, 404)
