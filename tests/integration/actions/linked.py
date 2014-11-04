from tests.test_cases import TestCase


class GetLinkedTestCase(TestCase):

    def test_app_should_respond_with_not_found_for_non_existing_link(self):
        response = self.client.get('/api/articles/4/links/categ')

        self.assertEqual(response.status_code, 404)


class GetLinkedBelongsToTestCase(TestCase):

    def test_app_should_respond_with_category(self):
        response = self.client.get('/api/articles/1/links/category')

        self.assertEqual(response.status_code, 200)

        categories = response.document.get('categories', None)

        self.assertIsNotNone(categories)
        self.assertIsInstance(categories, dict)

    def test_app_should_respond_with_empty_category(self):
        response = self.client.get('/api/articles/4/links/category')

        self.assertEqual(response.status_code, 200)

        categories = response.document.get('categories', None)

        self.assertIsNone(categories)


class GetLinkedHasManyTestCase(TestCase):

    def test_app_should_respond_with_articles(self):
        response = self.client.get('/api/categories/1/links/articles')

        self.assertEqual(response.status_code, 200)

        articles = response.document.get('articles', None)

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        self.assertTrue(len(articles) > 0)


class PostLinkedTestCase(TestCase):

    def test_app_should_post_category_on_article(self):
        data = {
            'categories': '1'
        }

        response = self.client.post('/api/articles/4/links/category', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/1')
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.document.get('articles').get('links').get('category'))

        response = self.client.get('/api/articles/1/links/category')
        categories = response.document.get('categories')
        self.assertIsNotNone(categories)

    def test_app_should_not_post_category_on_article_with_existing_one(self):
        data = {
            'categories': '1'
        }

        response = self.client.post('/api/articles/2/links/category', data)

        self.assertEquals(response.status_code, 409)

    def test_app_should_post_articles_on_category(self):
        data = {
            'articles': ['4', '5']
        }

        response = self.client.post('/api/categories/2/links/articles', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/4')
        category = response.document.get('articles').get('links').get('category')

        self.assertEqual(category, '2')

        response = self.client.get('/api/articles/5')
        category = response.document.get('articles').get('links').get('category')

        self.assertEqual(category, '2')

        response = self.client.get('/api/categories/2/links/articles')
        articles = response.document.get('articles')

        self.assertIsNotNone(articles)
        self.assertEqual(len(articles), 2)

    def test_app_should_not_post_articles_on_category_with_existing_ones(self):
        data = {
            'articles': ['1', '3']
        }

        response = self.client.post('/api/categories/1/links/articles', data)

        self.assertEquals(response.status_code, 409)


class PutLinkedTestCase(TestCase):

    def test_app_should_put_category_on_article(self):
        data = {
            'categories': '2'
        }

        response = self.client.put('/api/articles/1/links/category', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.document.get('articles').get('links').get('category'), '2')

        response = self.client.get('/api/articles/1/links/category')
        categories = response.document.get('categories')
        self.assertIsNotNone(categories)

    def test_app_should_post_articles_on_category(self):
        data = {
            'articles': ['1', '4']
        }

        response = self.client.post('/api/categories/2/links/articles', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/1')
        category = response.document.get('articles').get('links').get('category')

        self.assertEqual(category, '2')

        response = self.client.get('/api/articles/4')
        category = response.document.get('articles').get('links').get('category')

        self.assertEqual(category, '2')

        response = self.client.get('/api/categories/2/links/articles')
        articles = response.document.get('articles')

        self.assertIsNotNone(articles)
        self.assertEqual(len(articles), 2)


class DeleteLinkedBelongsToTestCase(TestCase):

    def test_app_should_delete_category_on_article(self):
        response = self.client.delete('/api/articles/1/links/category')

        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/articles/1/links/category')
        categories = response.document.get('categories', None)
        self.assertIsNone(categories)

        response = self.client.get('/api/articles/1')
        articles = response.document.get('articles', None)

        self.assertIsNone(articles.get('links').get('categories'))


class DeleteHasManyTestCase(TestCase):

    def test_app_should_not_delete_articles_on_category(self):
        response = self.client.get('/api/categories/1/links/articles')
        before_articles = response.document.get('articles')

        response = self.client.delete('/api/categories/1/links/articles')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/api/categories/1/links/articles')
        after_articles = response.document.get('articles')

        self.assertListEqual(after_articles, before_articles)
