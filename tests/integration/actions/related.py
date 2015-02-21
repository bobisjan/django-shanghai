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


class GetSortedRelatedTestCase(TestCase):

    def test_app_should_respond_with_sorted_tags_asc(self):
        response = self.client.get('/api/articles/1/tags?sort=%2Bname')

        self.assertEqual(response.status_code, 200)

        tags = response.document.get('data')

        self.assertIsNotNone(tags)
        self.assertIsInstance(tags, list)
        self.assertTrue(len(tags) > 0)

        first = tags[0]
        last = tags[len(tags) - 1]

        self.assertEqual(first.get('name'), 'aaa')
        self.assertEqual(last.get('name'), 'bbb')

    def test_app_should_respond_with_sorted_tags_desc(self):
        response = self.client.get('/api/articles/1/tags?sort=-name')

        self.assertEqual(response.status_code, 200)

        tags = response.document.get('data')

        self.assertIsNotNone(tags)
        self.assertIsInstance(tags, list)
        self.assertTrue(len(tags) > 0)

        first = tags[0]
        last = tags[len(tags) - 1]

        self.assertEqual(first.get('name'), 'bbb')
        self.assertEqual(last.get('name'), 'aaa')
