from tests.test_cases import TestCase


class GetRelatedTestCase(TestCase):

    def test_app_should_respond_with_not_found_for_non_existing_link(self):
        response = self.client.get('/api/articles/4/categ')

        self.assertEqual(response.status_code, 404)


class GetRelatedBelongsToTestCase(TestCase):

    def test_app_should_respond_with_category(self):
        response = self.client.get('/api/articles/1/category')

        self.assertEqual(response.status_code, 200)

        category = response.document.get('data')

        self.assertIsNotNone(category)
        self.assertIsInstance(category, dict)

    def test_app_should_respond_with_empty_category(self):
        response = self.client.get('/api/articles/4/category')

        self.assertEqual(response.status_code, 200)

        category = response.document.get('data')

        self.assertIsNone(category)


class GetRelatedHasManyTestCase(TestCase):

    def test_app_should_respond_with_articles(self):
        response = self.client.get('/api/categories/1/articles')

        self.assertEqual(response.status_code, 200)

        articles = response.document.get('data')

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        self.assertTrue(len(articles) > 0)
