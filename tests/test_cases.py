import json

from django import conf, test
from django.core.serializers.json import DjangoJSONEncoder

import shanghai
from shanghai.conf import settings


class Client(test.Client):

    def request(self, **request):
        response = super(Client, self).request(**request)

        if response.content:
            document = json.loads(response.content.decode(conf.settings.DEFAULT_CHARSET))
            setattr(response, 'document', document)

        return response

    def post(self, path, data=None, content_type=settings.CONTENT_TYPE, follow=False, secure=False, **extra):
        if data:
            data = json.dumps(data, cls=DjangoJSONEncoder)

        return super(Client, self).post(path,
                                        data=data,
                                        content_type=content_type,
                                        follow=follow,
                                        secure=secure,
                                        **extra)

    def patch(self, path, data='', content_type=settings.CONTENT_TYPE, follow=False, secure=False, **extra):
        if data:
            data = json.dumps(data, cls=DjangoJSONEncoder)

        return super(Client, self).patch(path,
                                         data=data,
                                         content_type=content_type,
                                         follow=follow,
                                         secure=secure,
                                         **extra)

    def delete(self, path, data='', content_type=settings.CONTENT_TYPE, follow=False, secure=False, **extra):
        if data:
            data = json.dumps(data, cls=DjangoJSONEncoder)

        return super(Client, self).delete(path,
                                          data=data,
                                          content_type=content_type,
                                          follow=follow,
                                          secure=secure,
                                          **extra)


class TestCase(test.TestCase):

    client_class = Client

    fixtures = ['data']

    def setUp(self):
        self.api = shanghai.api

    def assertObject(self, obj):
        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, dict)

        self.assertTrue('type' in obj)
        self.assertTrue('id' in obj)

        self.assertTrue('links' in obj)
        self.assertIsInstance(obj['links'], dict)

        self.assertTrue('self' in obj['links'])

    def assertSparseObject(self, obj, attributes, relationships):
        self.assertObject(obj)

        [self.assertTrue(inc in obj) for inc in attributes[0]]
        [self.assertFalse(inc in obj) for inc in attributes[1]]

        [self.assertTrue(inc in obj['links']) for inc in relationships[0]]
        [self.assertFalse(inc in obj['links']) for inc in relationships[1]]
