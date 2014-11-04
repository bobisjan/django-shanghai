import json

from django import test
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

import shanghai


class Client(test.Client):

    def request(self, **request):
        response = super(Client, self).request(**request)

        if response.content:
            document = json.loads(response.content.decode(settings.DEFAULT_CHARSET))
            setattr(response, 'document', document)

        return response

    def post(self, path, data=None, follow=False, secure=False, **extra):
        if data:
            data = json.dumps(data, cls=DjangoJSONEncoder)

        return super(Client, self).post(path,
                                        data=data,
                                        content_type=shanghai.CONTENT_TYPE,
                                        follow=follow,
                                        secure=secure,
                                        **extra)


class TestCase(test.TestCase):

    client_class = Client

    fixtures = ['data']

    def setUp(self):
        self.api = shanghai.api
