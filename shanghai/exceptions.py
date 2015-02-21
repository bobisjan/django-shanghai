from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError

from shanghai.http import HttpResponseConflict, JsonApiResponse


class BaseError(Exception):

    def get_response(self):
        return HttpResponseServerError()


class ConflictError(BaseError):

    def get_response(self):
        return HttpResponseConflict()


class ForbiddenError(BaseError):

    def get_response(self):
        return HttpResponseForbidden()


class NotFoundError(BaseError):

    def get_response(self):
        return HttpResponseNotFound()


class RelationshipDoesNotExist(NotFoundError):

    def __init__(self, resource, relationship):
        self.resource = resource
        self.relationship = relationship

    def __str__(self):
        return 'Relationship `{1}` does not exist on resource `{0}`.'.format(self.resource, self.relationship)


class LinkedResourceAlreadyExists(ConflictError):

    def __init__(self, resource, obj, relationship, link):
        self.resource = resource
        self.object = obj
        self.relationship = relationship
        self.link = link

    def __str__(self):
        return 'Relationship `{2}` on resource `{1}` of `{0}` already has been set with `{3}`.'.format(
            self.resource, self.object, self.relationship, self.link)


class TypeConflictError(ConflictError):

    def __init__(self, resource_type, data_type):
        self.resource_type = resource_type
        self.data_type = data_type

    def __str__(self):
        return 'Data type `{1}` does not match with resource type `{0}`.'.format(self.resource_type, self.data_type)


class ModelValidationError(BaseError):

    def __init__(self, error):
        self.error = error

    def get_response(self, **kwargs):
        kwargs.setdefault('status', 400)

        errors = list()

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
