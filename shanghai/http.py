from django.http import HttpResponse, JsonResponse

from shanghai.conf import settings


class JsonApiResponse(JsonResponse):

    def __init__(self, data, **kwargs):
        kwargs.setdefault('content_type', settings.CONTENT_TYPE)
        super(JsonApiResponse, self).__init__(data=data, **kwargs)


class HttpResponseNoContent(HttpResponse):

    status_code = 204


class HttpResponseConflict(HttpResponse):

    status_code = 409


class HttpResponseNotImplemented(HttpResponse):

    status_code = 501
