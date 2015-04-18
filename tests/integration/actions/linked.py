from tests.test_cases import TestCase


class PostLinkedTestCase(TestCase):

    def test_app_should_not_post_category_on_article(self):
        data = {
            'data': {
                'type': 'categories',
                'id': '1'
            }
        }

        response = self.client.post('/api/articles/2/links/category', data)

        self.assertEquals(response.status_code, 403)

    def test_app_should_post_articles_on_category(self):
        data = {
            'data': {
                'type': 'articles',
                'ids': ['4', '5']
            }
        }

        response = self.client.post('/api/categories/2/links/articles', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/4')
        category = response.document.get('data').get('links').get('category')

        linkage = category.get('linkage')
        self.assertEqual(linkage.get('id'), '2')
        self.assertEqual(linkage.get('type'), 'categories')

        response = self.client.get('/api/articles/5')
        category = response.document.get('data').get('links').get('category')

        linkage = category.get('linkage')
        self.assertEqual(linkage.get('id'), '2')
        self.assertEqual(linkage.get('type'), 'categories')

        response = self.client.get('/api/categories/2/articles')
        articles = response.document.get('data')

        self.assertIsNotNone(articles)
        self.assertEqual(len(articles), 2)

    def test_app_should_post_articles_on_category_using_links(self):
        data = {
            'data': {
                'type': 'articles',
                'ids': ['1', '4']
            }
        }

        response = self.client.post('/api/categories/2/links/articles', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/1')
        category = response.document.get('data').get('links').get('category')

        linkage = category.get('linkage')
        self.assertEqual(linkage.get('id'), '2')
        self.assertEqual(linkage.get('type'), 'categories')

        response = self.client.get('/api/articles/4')
        category = response.document.get('data').get('links').get('category')

        linkage = category.get('linkage')
        self.assertEqual(linkage.get('id'), '2')
        self.assertEqual(linkage.get('type'), 'categories')

        response = self.client.get('/api/categories/2/articles')
        articles = response.document.get('data')

        self.assertIsNotNone(articles)
        self.assertEqual(len(articles), 2)

    def test_app_should_not_post_articles_on_category_with_already_set_ones(self):
        data = {
            'data': {
                'type': 'articles',
                'ids': ['1', '3']
            }
        }

        response = self.client.post('/api/categories/1/links/articles', data)

        self.assertEquals(response.status_code, 403)


class PutLinkedTestCase(TestCase):

    def test_app_should_put_category_on_article_using_links(self):
        data = {
            'data': {
                'type': 'categories',
                'id': '2'
            }
        }

        response = self.client.put('/api/articles/1/links/category', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/1')
        self.assertEqual(response.status_code, 200)

        category = response.document.get('data').get('links').get('category')

        linkage = category.get('linkage')
        self.assertEqual(linkage.get('id'), '2')
        self.assertEqual(linkage.get('type'), 'categories')

        response = self.client.get('/api/articles/1/category')
        self.assertIsNotNone(response.document.get('data'))

    def test_app_should_put_articles_on_category_using_links(self):
        data = {
            'data': {
                'type': 'articles',
                'ids': ['1', '4']
            }
        }

        response = self.client.put('/api/categories/2/links/articles', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/1')
        category = response.document.get('data').get('links').get('category')

        linkage = category.get('linkage')
        self.assertEqual(linkage.get('id'), '2')
        self.assertEqual(linkage.get('type'), 'categories')

        response = self.client.get('/api/articles/4')
        category = response.document.get('data').get('links').get('category')

        linkage = category.get('linkage')
        self.assertEqual(linkage.get('id'), '2')
        self.assertEqual(linkage.get('type'), 'categories')

        response = self.client.get('/api/categories/2/articles')
        articles = response.document.get('data')

        self.assertIsNotNone(articles)
        self.assertEqual(len(articles), 2)


class DeleteHasManyTestCase(TestCase):

    def test_app_should_delete_articles_on_category(self):
        data = {
            'data': {
                'type': 'articles',
                'ids': ['1', '2', '3']
            }
        }

        response = self.client.delete('/api/categories/1/links/articles', data)
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/categories/1/articles')
        after_articles = response.document.get('data')

        self.assertListEqual(after_articles, [])
