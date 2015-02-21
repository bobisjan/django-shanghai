from tests.test_cases import TestCase


class GetObjectTestCase(TestCase):

    def test_app_should_respond_with_article(self):
        response = self.client.get('/api/articles/1')

        self.assertEqual(response.status_code, 200)

        article = response.document.get('data', None)

        self.assertIsNotNone(article)
        self.assertIsInstance(article, dict)

        links = article.get('links')

        self.assertEqual(links.get('self'), 'http://testserver/api/articles/1')

        category = links.get('category')

        self.assertEqual(category.get('type'), 'categories')
        self.assertEqual(category.get('id'), '1')
        self.assertEqual(category.get('self'), 'http://testserver/api/articles/1/links/category')
        self.assertEqual(category.get('resource'), 'http://testserver/api/articles/1/category')

        tags = links.get('tags')

        self.assertEqual(tags.get('type'), 'tags')
        self.assertListEqual(tags.get('ids'), ['1', '2'])
        self.assertEqual(tags.get('self'), 'http://testserver/api/articles/1/links/tags')
        self.assertEqual(tags.get('resource'), 'http://testserver/api/articles/1/tags')



class GetEmptyObjectTestCase(TestCase):

    fixtures = None

    def test_app_should_return_not_found(self):
        response = self.client.get('/api/articles/30')

        self.assertEqual(response.status_code, 404)


class PutObjectTestCase(TestCase):

    def test_app_should_put_article(self):
        data = {
            'data': {
                'type': 'articles',
                'id': '1',
                'title': 'Updated title'
            }
        }

        response = self.client.put('/api/articles/1', data)

        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/articles/1')

        self.assertEqual(response.document.get('data').get('title'), 'Updated title')

    def test_app_should_put_category_on_article(self):
        data = {
            'data': {
                'type': 'articles',
                'id': '1',
                'links': {
                    'category': {
                        'type': 'categories',
                        'id': '2'
                    }
                }
            }
        }

        response = self.client.put('/api/articles/1', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.document.get('data').get('links').get('category').get('id'), '2')

        response = self.client.get('/api/articles/1/category')
        self.assertIsNotNone(response.document.get('data'))
        self.assertEqual(response.document.get('data').get('id'), '2')


    def test_app_should_put_articles_on_category(self):
        data = {
            'data': {
                'type': 'categories',
                'id': '2',
                'links': {
                    'articles': {
                        'type': 'articles',
                        'ids': ['1', '4']
                    }
                }
            }
        }

        response = self.client.put('/api/categories/2', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/1')
        category = response.document.get('data').get('links').get('category')

        self.assertEqual(category.get('id'), '2')

        response = self.client.get('/api/articles/4')
        category = response.document.get('data').get('links').get('category')

        self.assertEqual(category.get('id'), '2')

        response = self.client.get('/api/categories/2/articles')
        articles = response.document.get('data')

        self.assertIsNotNone(articles)
        self.assertEqual(len(articles), 2)


class DeleteObjectTestCase(TestCase):

    def test_app_should_delete_article(self):
        response = self.client.delete('/api/articles/3')
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/articles/3')
        self.assertEqual(response.status_code, 404)

    def test_app_should_respond_with_not_found_for_non_existing_article(self):
        response = self.client.delete('/api/articles/105')
        self.assertEqual(response.status_code, 404)
