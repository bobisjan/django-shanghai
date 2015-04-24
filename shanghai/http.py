from django.http import HttpResponse


class HttpResponseNoContent(HttpResponse):

    status_code = 204


class HttpResponseConflict(HttpResponse):

    status_code = 409


class HttpResponseNotImplemented(HttpResponse):

    status_code = 501
