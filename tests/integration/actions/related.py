from tests.test_cases import TestCase


class GetRelatedTestCase(TestCase):

    def test_app_should_respond_with_not_found_for_non_existing_link(self):
        response = self.client.get('/api/articles/4/categ')

        self.assertEqual(response.status_code, 404)


class GetRelatedBelongsToTestCase(TestCase):

    def test_app_should_respond_with_category(self):
        response = self.client.get('/api/articles/1/category')

        self.assertEqual(response.status_code, 200)

        meta = response.document.get('meta', None)
        self.assertIsNone(meta)

        links = response.document.get('links')
        self.assertEqual(links.get('self'), 'http://testserver/api/articles/1/category')

        category = response.document.get('data')

        self.assertIsNotNone(category)
        self.assertIsInstance(category, dict)

        links = category.get('links')
        self.assertEqual(links.get('self'), 'http://testserver/api/categories/1')

        included = response.document.get('included', None)
        self.assertIsNone(included)

    def test_app_should_respond_with_empty_category(self):
        response = self.client.get('/api/articles/4/category')

        self.assertEqual(response.status_code, 200)

        category = response.document.get('data')

        self.assertIsNone(category)


class GetSparseRelatedBelongsToTestCase(TestCase):

    def test_app_should_respond_with_sparse_category(self):
        response = self.client.get('/api/articles/1/category?fields[categories]=name')
        category = response.document.get('data')

        self.assertSparseObject(category, (('name',), ()), ((), ('articles',)))


class GetRelatedHasManyTestCase(TestCase):

    def test_app_should_respond_with_articles(self):
        response = self.client.get('/api/categories/1/articles')

        self.assertEqual(response.status_code, 200)

        meta = response.document.get('meta', None)
        self.assertIsNone(meta)

        links = response.document.get('links')
        self.assertEqual(links.get('self'), 'http://testserver/api/categories/1/articles')

        articles = response.document.get('data')

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        self.assertTrue(len(articles) > 0)

        for article in articles:
            links = article.get('links')
            self.assertEqual(links.get('self'), 'http://testserver/api/articles/' + article.get('id'))

        included = response.document.get('included', None)
        self.assertIsNone(included)


class GetFilteredRelatedTestCase(TestCase):

    def test_app_should_respond_with_filtered_tags(self):
        response = self.client.get('/api/articles/1/tags?filter[name]=aaa')

        self.assertEqual(response.status_code, 200)

        tags = response.document.get('data')

        self.assertIsNotNone(tags)
        self.assertIsInstance(tags, list)
        self.assertEqual(len(tags), 1)

        self.assertEqual(tags[0].get('name'), 'aaa')


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


class GetPaginatedHasManyTestCase(TestCase):

    def test_app_should_respond_with_paginated_has_many(self):
        response = self.client.get('/api/articles/1/tags?page%5Boffset%5D=0&page%5Blimit%5D=2')
        self.assertEqual(response.status_code, 200)

        tags = response.document.get('data')
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0].get('id'), '1')
        self.assertEqual(tags[1].get('id'), '2')

        links = response.document.get('links')
        self.assertEqual(links.get('first'), 'http://testserver/api/articles/1/tags?page[offset]=0&page[limit]=2')
        self.assertIsNone(links.get('prev'))
        self.assertIsNone(links.get('next'))
        self.assertEqual(links.get('last'), 'http://testserver/api/articles/1/tags?page[offset]=0&page[limit]=2')


class GetSparseHasManyTestCase(TestCase):

    def test_app_should_respond_with_sparse_tags(self):
        response = self.client.get('/api/articles/1/tags?fields[tags]=name')
        tags = response.document.get('data')

        for tag in tags:
            self.assertSparseObject(tag, (('name',), []), ([], ('articles',)))


class GetIncludedRelatedBelongsToTestCase(TestCase):

    def test_app_should_respond_with_related_category_and_included(self):
        response = self.client.get('/api/articles/1/category?include=articles')

        self.assertEqual(response.status_code, 200)

        included = response.document.get('included', None)
        self.assertIsNotNone(included)
        [self.assertEqual('articles', item['type']) for item in included]


class GetIncludedRelatedHasManyTestCase(TestCase):

    def test_app_should_respond_with_related_articles_and_included(self):
        response = self.client.get('/api/categories/1/articles?include=category')

        self.assertEqual(response.status_code, 200)

        included = response.document.get('included', None)
        self.assertIsNotNone(included)
        [self.assertEqual('categories', item['type']) for item in included]
