from tests.test_cases import TestCase


class GetCollectionTestCase(TestCase):

    def test_app_should_respond_with_articles(self):
        response = self.client.get('/api/articles')

        self.assertEqual(response.status_code, 200)

        articles = response.document.get('articles')

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        self.assertTrue(len(articles) > 0)


class GetEmptyCollectionTestCase(TestCase):

    fixtures = None

    def test_app_should_return_empty_array(self):
        response = self.client.get('/api/articles')

        self.assertEqual(response.status_code, 200)

        articles = response.document.get('articles')

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        self.assertEqual(len(articles), 0)


class PostCollectionTestCase(TestCase):

    def test_app_should_create_article(self):
        data = {
            'articles': {
                'title': 'Lorem ipsum',
                'perex': 'Lorem ipsum...',
                'links': {
                    'category': '1'
                }
            }
        }

        response = self.client.post('/api/articles', data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], 'http://testserver/api/articles/6')

        response = self.client.get('/api/articles/6')

        self.assertEquals(response.status_code, 200)

        articles = response.document.get('articles')
        self.assertIsNotNone(articles)

    def test_app_should_create_articles(self):
        data = {
            'articles': [{
                'title': 'Lorem ipsum #1',
                'perex': 'Lorem ipsum #1...',
                'links': {
                    'category': None
                }
            }, {
                'title': 'Lorem ipsum #2',
                'perex': 'Lorem ipsum #2...',
                'links': {
                    'category': '1'
                }
            }]
        }

        response = self.client.post('/api/articles', data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], 'http://testserver/api/articles/6,7')

        response = self.client.get('/api/articles/6,7')
        self.assertEquals(response.status_code, 200)

        response = self.client.get('/api/articles/6')
        self.assertEquals(response.status_code, 200)

        response = self.client.get('/api/articles/7')
        self.assertEquals(response.status_code, 200)
