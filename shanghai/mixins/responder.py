from shanghai.http import JsonApiResponse


class ResponderMixin(object):

    def response(self, data, serializer=None, **kwargs):
        if not serializer:
            serializer = getattr(self, 'serializer')

        serialized_data = serializer.serialize(data)
        return JsonApiResponse(serialized_data, **kwargs)
