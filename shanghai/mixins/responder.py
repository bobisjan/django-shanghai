import logging

from django.http import HttpResponseServerError

from shanghai.http import JsonApiResponse
from shanghai.utils import is_iterable


logger = logging.getLogger(__name__)


class ResponderMixin(object):

    def response(self, data, serializer=None, **kwargs):
        if not serializer:
            serializer = getattr(self, 'serializer')

        serialized_data = serializer.serialize(data, **kwargs)

        if 'links' in kwargs:
            del kwargs['links']

        return JsonApiResponse(serialized_data, **kwargs)

    def response_with_location(self, object_or_iterable):
        response = self.response(object_or_iterable, status=201)

        if not is_iterable(object_or_iterable):
            object_or_iterable = [object_or_iterable]

        pks = list()
        _id = self.primary_key()

        for obj in object_or_iterable:
            pk = _id.get_from(obj)
            pk = self.serializer.normalize_id(pk)
            pks.append(pk)

        if len(pks) > 1:
            pk = ','.join(pk)
        else:
            pk = pks[0]

        location = self.reverse_url(pk=pk)
        response['Location'] = location

        return response

    def response_with_error(self, error):
        get_response = getattr(error, 'get_response', None)

        if get_response is None:
            logger.exception(error)
            return HttpResponseServerError()

        logger.error(error)
        return get_response()
