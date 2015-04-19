from tests.test_cases import TestCase


class GetCollectionTestCase(TestCase):

    def test_app_should_respond_with_articles(self):
        response = self.client.get('/api/articles')

        self.assertEqual(response.status_code, 200)

        meta = response.document.get('meta', None)
        self.assertIsNone(meta)

        links = response.document.get('links')
        self.assertIsNotNone(links)
        self.assertEqual(links.get('self'), 'http://testserver/api/articles')

        articles = response.document.get('data')

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        self.assertTrue(len(articles) > 0)

        included = response.document.get('included', None)
        self.assertIsNone(included)


class GetEmptyCollectionTestCase(TestCase):

    fixtures = None

    def test_app_should_return_empty_array(self):
        response = self.client.get('/api/articles')

        self.assertEqual(response.status_code, 200)

        meta = response.document.get('meta', None)
        self.assertIsNone(meta)

        links = response.document.get('links')
        self.assertIsNotNone(links)
        self.assertEqual(links.get('self'), 'http://testserver/api/articles')

        articles = response.document.get('data')

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        self.assertEqual(len(articles), 0)

        included = response.document.get('included', None)
        self.assertIsNone(included)


class GetFilteredCollectionTestCase(TestCase):

    def test_app_should_respond_with_filtered_articles(self):
        response = self.client.get('/api/articles?filter[title:startswith]=Se')

        self.assertEqual(response.status_code, 200)

        articles = response.document.get('data')

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        self.assertEqual(len(articles), 1)

        self.assertEqual(articles[0].get('title'), 'Second article')


class GetSortedCollectionTestCase(TestCase):

    def test_app_should_respond_with_sorted_articles_asc(self):
        response = self.client.get('/api/articles?sort=%2Btitle')

        self.assertEqual(response.status_code, 200)

        articles = response.document.get('data')

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        self.assertTrue(len(articles) > 0)

        first = articles[0]
        last = articles[len(articles) - 1]

        self.assertEqual(first.get('title'), 'Fifth article')
        self.assertEqual(last.get('title'), 'Third article')

    def test_app_should_respond_with_sorted_articles_desc(self):
        response = self.client.get('/api/articles?sort=-title')

        self.assertEqual(response.status_code, 200)

        articles = response.document.get('data')

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        self.assertTrue(len(articles) > 0)

        first = articles[0]
        last = articles[len(articles) - 1]

        self.assertEqual(first.get('title'), 'Third article')
        self.assertEqual(last.get('title'), 'Fifth article')


class GetPaginatedCollectionTestCase(TestCase):

    def test_app_should_respond_with_paginated_articles(self):
        response = self.client.get('/api/articles?page%5Boffset%5D=0&page%5Blimit%5D=2')
        self.assertEqual(response.status_code, 200)

        articles = response.document.get('data')
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].get('id'), '1')
        self.assertEqual(articles[1].get('id'), '2')

        links = response.document.get('links')
        self.assertEqual(links.get('first'), 'http://testserver/api/articles?page[offset]=0&page[limit]=2')
        self.assertIsNone(links.get('prev'))
        self.assertEqual(links.get('next'), 'http://testserver/api/articles?page[offset]=2&page[limit]=2')
        self.assertEqual(links.get('last'), 'http://testserver/api/articles?page[offset]=4&page[limit]=2')

        response = self.client.get('/api/articles?page%5Boffset%5D=2&page%5Blimit%5D=2')
        self.assertEqual(response.status_code, 200)

        articles = response.document.get('data')
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].get('id'), '3')
        self.assertEqual(articles[1].get('id'), '4')

        links = response.document.get('links')
        self.assertEqual(links.get('first'), 'http://testserver/api/articles?page[offset]=0&page[limit]=2')
        self.assertEqual(links.get('prev'), 'http://testserver/api/articles?page[offset]=0&page[limit]=2')
        self.assertEqual(links.get('next'), 'http://testserver/api/articles?page[offset]=4&page[limit]=2')
        self.assertEqual(links.get('last'), 'http://testserver/api/articles?page[offset]=4&page[limit]=2')

        response = self.client.get('/api/articles?page%5Boffset%5D=4&page%5Blimit%5D=2')
        self.assertEqual(response.status_code, 200)

        articles = response.document.get('data')
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].get('id'), '5')

        links = response.document.get('links')
        self.assertEqual(links.get('first'), 'http://testserver/api/articles?page[offset]=0&page[limit]=2')
        self.assertEqual(links.get('prev'), 'http://testserver/api/articles?page[offset]=2&page[limit]=2')
        self.assertIsNone(links.get('next'))
        self.assertEqual(links.get('last'), 'http://testserver/api/articles?page[offset]=4&page[limit]=2')


class PostCollectionTestCase(TestCase):

    def test_app_should_create_article(self):
        data = {
            'data': {
                'type': 'articles',
                'title': 'Lorem ipsum',
                'perex': 'Lorem ipsum...',
                'links': {
                    'category': {
                        'linkage': {
                            'type': 'categories',
                            'id': '1'
                        }
                    }
                }
            }
        }

        response = self.client.post('/api/articles', data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Location'], 'http://testserver/api/articles/6')

        response = self.client.get('/api/articles/6')

        self.assertEquals(response.status_code, 200)

        article = response.document.get('data')
        self.assertIsNotNone(article)
