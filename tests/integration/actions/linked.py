from tests.test_cases import TestCase


class GetLinkedTestCase(TestCase):

    def test_app_should_respond_with_not_found_for_non_existing_link(self):
        response = self.client.get('/api/articles/4/links/categ')

        self.assertEqual(response.status_code, 404)


class GetLinkedBelongsToTestCase(TestCase):

    def test_app_should_respond_with_category(self):
        response = self.client.get('/api/articles/1/links/category')

        self.assertEqual(response.status_code, 200)

        meta = response.document.get('meta', None)
        self.assertIsNone(meta)

        links = response.document.get('links')
        self.assertEqual(links.get('self'), 'http://testserver/api/articles/1/links/category')
        self.assertEqual(links.get('related'), 'http://testserver/api/articles/1/category')

        category = response.document.get('data')

        self.assertIsNotNone(category)
        self.assertIsInstance(category, dict)
        self.assertEqual(category.get('type'), 'categories')
        self.assertEqual(category.get('id'), '1')

        included = response.document.get('included', None)
        self.assertIsNone(included)

    def test_app_should_respond_with_empty_category(self):
        response = self.client.get('/api/articles/4/links/category')

        self.assertEqual(response.status_code, 200)

        category = response.document.get('data')

        self.assertIsNone(category)


class GetLinkedHasManyTestCase(TestCase):

    def test_app_should_respond_with_articles(self):
        response = self.client.get('/api/categories/1/links/articles')

        self.assertEqual(response.status_code, 200)

        meta = response.document.get('meta', None)
        self.assertIsNone(meta)

        links = response.document.get('links')
        self.assertEqual(links.get('self'), 'http://testserver/api/categories/1/links/articles')

        articles = response.document.get('data')

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        self.assertTrue(len(articles) > 0)

        self.assertEqual(articles[0].get('id'), '1')
        self.assertEqual(articles[1].get('id'), '2')

        included = response.document.get('included', None)
        self.assertIsNone(included)


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
            'data': [{
                'type': 'articles',
                'id': '4'
            }, {
                'type': 'articles',
                'id': '5'
            }]
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
            'data': [{
                'type': 'articles',
                'id': '1'
            }, {
                'type': 'articles',
                'id': '4'
            }]
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
            'data': [{
                'type': 'articles',
                'id': '1'
            }, {
                'type': 'articles',
                'id': '3'
            }]
        }

        response = self.client.post('/api/categories/1/links/articles', data)

        self.assertEquals(response.status_code, 403)


class PatchLinkedTestCase(TestCase):

    def test_app_should_patch_category_on_article_using_links(self):
        data = {
            'data': {
                'type': 'categories',
                'id': '2'
            }
        }

        response = self.client.patch('/api/articles/1/links/category', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/1')
        self.assertEqual(response.status_code, 200)

        category = response.document.get('data').get('links').get('category')

        linkage = category.get('linkage')
        self.assertEqual(linkage.get('id'), '2')
        self.assertEqual(linkage.get('type'), 'categories')

        response = self.client.get('/api/articles/1/category')
        self.assertIsNotNone(response.document.get('data'))

    def test_app_should_patch_articles_on_category_using_links(self):
        data = {
            'data': [{
                'type': 'articles',
                'id': '1'
            }, {
                'type': 'articles',
                'id': '4'
            }]
        }

        response = self.client.patch('/api/categories/2/links/articles', data)

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
            'data': [{
                'type': 'articles',
                'id': '1'
            }, {
                'type': 'articles',
                'id': '2'
            }, {
                'type': 'articles',
                'id': '3'
            }]
        }

        response = self.client.delete('/api/categories/1/links/articles', data)
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/categories/1/articles')
        after_articles = response.document.get('data')

        self.assertListEqual(after_articles, [])
