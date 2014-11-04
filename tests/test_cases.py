import json

from django import test
from django.conf import settings

import shanghai


class Client(test.Client):

    def request(self, **request):
        response = super(Client, self).request(**request)

        if response.content:
            document = json.loads(response.content.decode(settings.DEFAULT_CHARSET))
            setattr(response, 'document', document)

        return response


class TestCase(test.TestCase):

    client_class = Client

    fixtures = ['data']

    def setUp(self):
        self.api = shanghai.api
