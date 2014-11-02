from django.core.exceptions import ValidationError

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

    def response_with_error(self, error, **kwargs):
        kwargs.setdefault('status', 400)

        errors = list()

        if isinstance(error, ValidationError):
            validation_errors = self.from_validation_error(error, **kwargs)
            errors.extend(validation_errors)

        return JsonApiResponse(dict(errors=errors), **kwargs)

    def from_validation_error(self, error, **kwargs):
        errors = list()

        if hasattr(error, 'error_dict'):
            for key, error_list in error.message_dict.items():
                for _error in error_list:
                    errors.append(self.error_dict(key, kwargs['status'], _error))

        return errors

    @staticmethod
    def error_dict(id, status, title, **kwargs):
        error = dict(
            id=id,
            status=status,
            title=title
        )

        error.update(**kwargs)

        return error
