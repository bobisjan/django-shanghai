from shanghai.http import JsonApiResponse
from shanghai.utils import is_iterable


class ResponderMixin(object):

    def response(self, data, serializer=None, **kwargs):
        if not serializer:
            serializer = getattr(self, 'serializer')

        serialized_data = serializer.serialize(data)

        return JsonApiResponse(serialized_data, **kwargs)

    def response_with_location(self, object_or_iterable):
        response = self.response(object_or_iterable, status=201)

        if not is_iterable(object_or_iterable):
            object_or_iterable = [object_or_iterable]

        pk = list()
        _id = self.get_id()

        for obj in object_or_iterable:
            _pk = _id.get_from(obj)
            _pk = self.serializer.normalize_id(_pk)
            pk.append(_pk)

        if len(pk) > 1:
            pk = ','.join(pk)
        else:
            pk = pk[0]

        location = self.reverse_url(pk=pk)
        response['Location'] = location

        return response
