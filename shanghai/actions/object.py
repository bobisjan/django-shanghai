from django.db import transaction
from django.http import HttpResponseNotFound

from shanghai.http import HttpResponseNoContent


class ObjectMixin(object):

    def get_object(self):
        obj = self.fetch_object()
        return self.response(obj)

    def patch_object(self):
        obj = self.fetch_object()
        data = self.resolve_object_input()

        # TODO check self.pk with data.pk

        updated_object = self.patch_object_data(obj, data)

        if updated_object:
            return self.response(updated_object)

        return HttpResponseNoContent()

    def patch_object_data(self, obj, data):
        raise NotImplementedError()

    def delete_object(self):
        obj = self.fetch_object()
        self.delete_object_data(obj)
        return HttpResponseNoContent()

    def delete_object_data(self, obj):
        raise NotImplementedError()

    def resolve_object_input(self):
        return self.serializer.extract(self.input)


class ModelObjectMixin(ObjectMixin):

    def patch_object_data(self, obj, data):
        with transaction.atomic():
            self.save_object(obj, data)

    def delete_object_data(self, obj):
        self.remove_object(obj)
