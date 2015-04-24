import logging

from django.http import HttpResponseServerError, JsonResponse

from shanghai.conf import settings
from shanghai.utils import is_iterable


logger = logging.getLogger(__name__)


class ResponderMixin(object):

    def response(self, object_or_iterable, serializer=None, parent=None, linked=None, related=None, **kwargs):
        if not serializer:
            serializer = getattr(self, 'serializer')

        serialized_data = serializer.serialize(object_or_iterable, parent, linked, related, **kwargs)

        parameters = self.response_parameters(object_or_iterable, serializer, parent, linked, related, **kwargs)
        response = JsonResponse(serialized_data, **parameters)

        headers = self.response_headers(object_or_iterable, serializer, parent, linked, related, **kwargs)
        for key, value in headers.items():
            response[key] = value

        return response

    def response_parameters(self, object_or_iterable, serializer=None, parent=None, linked=None, related=None, **kwargs):
        parameters = dict()

        parameters.setdefault('content_type', settings.CONTENT_TYPE)

        if self.is_post_collection():
            parameters['status'] = 201

        return parameters

    def response_headers(self, object_or_iterable, serializer=None, parent=None, linked=None, related=None, **kwargs):
        headers = dict()

        if self.is_post_collection():
            headers['Location'] = self.location_for(object_or_iterable)

        return headers

    def location_for(self, object_or_iterable):
        if not is_iterable(object_or_iterable):
            object_or_iterable = [object_or_iterable]

        pks = list()
        primary_key = self.primary_key()

        for obj in object_or_iterable:
            pk = primary_key.get_from(obj)
            pk = self.serializer.normalize_id(pk)
            pks.append(pk)

        if len(pks) > 1:
            pk = ','.join(pk)
        else:
            pk = pks[0]

        return self.reverse_url(pk=pk)

    def response_with_error(self, error):
        get_response = getattr(error, 'get_response', None)

        if get_response is None:
            logger.exception(error)
            return HttpResponseServerError()

        logger.error(error)
        return get_response()
