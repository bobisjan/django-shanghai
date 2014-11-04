from django.http import HttpResponse, JsonResponse

import shanghai


class JsonApiResponse(JsonResponse):

    def __init__(self, data, **kwargs):
        kwargs.setdefault('content_type', shanghai.CONTENT_TYPE)
        super(JsonApiResponse, self).__init__(data=data, **kwargs)


class HttpResponseNoContent(HttpResponse):

    status_code = 204


class HttpResponseConflict(HttpResponse):

    status_code = 409


class HttpResponseNotImplemented(HttpResponse):

    status_code = 501
