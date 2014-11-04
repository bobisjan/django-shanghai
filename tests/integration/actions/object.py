from tests.test_cases import TestCase


class GetObjectTestCase(TestCase):

    def test_app_should_respond_with_article(self):
        response = self.client.get('/api/articles/1')

        self.assertEqual(response.status_code, 200)

        articles = response.document.get('articles', None)

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, dict)


class GetEmptyObjectTestCase(TestCase):

    fixtures = None

    def test_app_should_return_not_found(self):
        response = self.client.get('/api/articles/30')

        self.assertEqual(response.status_code, 404)


class PutObjectTestCase(TestCase):

    def test_app_should_put_article(self):
        data = {
            'articles': {
                'title': 'Updated title'
            }
        }

        response = self.client.put('/api/articles/1', data)

        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/articles/1')

        self.assertEqual(response.document.get('articles').get('title'), 'Updated title')


class DeleteObjectTestCase(TestCase):

    def test_app_should_delete_article(self):
        response = self.client.delete('/api/articles/3')
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/articles/3')
        self.assertEqual(response.status_code, 404)

    def test_app_should_respond_with_not_found_for_non_existing_article(self):
        response = self.client.delete('/api/articles/105')
        self.assertEqual(response.status_code, 404)
