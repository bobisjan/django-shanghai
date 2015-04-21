from tests.test_cases import TestCase


class GetObjectTestCase(TestCase):

    def test_app_should_respond_with_article(self):
        response = self.client.get('/api/articles/1')

        self.assertEqual(response.status_code, 200)

        meta = response.document.get('meta', None)
        self.assertIsNone(meta)

        article = response.document.get('data', None)

        self.assertIsNotNone(article)
        self.assertIsInstance(article, dict)

        links = article.get('links')
        self.assertEqual(links.get('self'), 'http://testserver/api/articles/1')

        category = links.get('category')
        linkage = category.get('linkage')

        self.assertEqual(linkage.get('type'), 'categories')
        self.assertEqual(linkage.get('id'), '1')

        self.assertEqual(category.get('self'), 'http://testserver/api/articles/1/links/category')
        self.assertEqual(category.get('related'), 'http://testserver/api/articles/1/category')

        tags = links.get('tags')
        linkage = tags.get('linkage')

        self.assertListEqual(linkage, [{'type': 'tags', 'id': '1'}, {'type': 'tags', 'id': '2'}])
        self.assertEqual(tags.get('self'), 'http://testserver/api/articles/1/links/tags')
        self.assertEqual(tags.get('related'), 'http://testserver/api/articles/1/tags')

        included = response.document.get('included', None)
        self.assertIsNone(included)


class GetEmptyObjectTestCase(TestCase):

    fixtures = None

    def test_app_should_return_not_found(self):
        response = self.client.get('/api/articles/30')

        self.assertEqual(response.status_code, 404)


class GetIncludedObjectTestCase(TestCase):

    def test_app_should_respond_with_article_and_included(self):
        response = self.client.get('/api/articles/1?include=category')
        included = response.document.get('included', None)
        self.assertIsNotNone(included)
        [self.assertEqual('categories', item['type']) for item in included]


class PatchObjectTestCase(TestCase):

    def test_app_should_patch_article(self):
        data = {
            'data': {
                'type': 'articles',
                'id': '1',
                'title': 'Updated title'
            }
        }

        response = self.client.patch('/api/articles/1', data)

        self.assertEqual(response.status_code, 204)

        response = self.client.get('/api/articles/1')

        self.assertEqual(response.document.get('data').get('title'), 'Updated title')

    def test_app_should_patch_category_on_article(self):
        data = {
            'data': {
                'type': 'articles',
                'id': '1',
                'links': {
                    'category': {
                        'linkage': {
                            'type': 'categories',
                            'id': '2'
                        }
                    }
                }
            }
        }

        response = self.client.patch('/api/articles/1', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/1')
        self.assertEqual(response.status_code, 200)

        links = response.document.get('data').get('links')
        category = links.get('category')

        self.assertEqual(category.get('linkage').get('id'), '2')
        self.assertEqual(category.get('linkage').get('type'), 'categories')

        response = self.client.get('/api/articles/1/category')
        self.assertIsNotNone(response.document.get('data'))
        self.assertEqual(response.document.get('data').get('id'), '2')

    def test_app_should_patch_articles_on_category(self):
        data = {
            'data': {
                'type': 'categories',
                'id': '2',
                'links': {
                    'articles': {
                        'linkage': [{
                            'type': 'articles',
                            'id': '1'
                        }, {
                            'type': 'articles',
                            'id': '4'
                        }]
                    }
                }
            }
        }

        response = self.client.patch('/api/categories/2', data)

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/articles/1')
        category = response.document.get('data').get('links').get('category')

        self.assertEqual(category.get('linkage').get('id'), '2')
        self.assertEqual(category.get('linkage').get('type'), 'categories')

        response = self.client.get('/api/articles/4')
        category = response.document.get('data').get('links').get('category')

        self.assertEqual(category.get('linkage').get('id'), '2')
        self.assertEqual(category.get('linkage').get('type'), 'categories')

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
