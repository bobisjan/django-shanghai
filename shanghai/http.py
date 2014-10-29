from django.http import HttpResponse, JsonResponse


class JsonApiResponse(JsonResponse):

    def __init__(self, data, **kwargs):
        kwargs.setdefault('content_type', 'application/vnd.api+json')
        super(JsonApiResponse, self).__init__(data=data, **kwargs)


class HttpResponseNoContent(HttpResponse):

    status_code = 204


class HttpResponseNotImplemented(HttpResponse):

    status_code = 501
