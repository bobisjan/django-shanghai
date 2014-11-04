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
