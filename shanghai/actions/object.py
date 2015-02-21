from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponseNotFound

from shanghai.exceptions import NotFoundError
from shanghai.http import HttpResponseNoContent


class ObjectMixin(object):

    def get_object_data(self, pk=None):
        raise NotImplementedError()

    def object_input_data(self):
        return self.serializer.extract(self.input)

    def get_object(self):
        obj = self.get_object_data()

        return self.response(obj)

    def put_object(self):
        obj = self.get_object_data()
        data = self.object_input_data()

        # TODO check self.pk with data.pk

        updated_object = self.put_object_data(obj, data)

        if updated_object:
            return self.response(updated_object)

        return HttpResponseNoContent()

    def put_object_data(self, obj, data):
        raise NotImplementedError()

    def delete_object(self):
        obj = self.get_object_data()

        self.delete_object_data(obj)

        return HttpResponseNoContent()

    def delete_object_data(self, obj):
        raise NotImplementedError()


class ModelObjectMixin(ObjectMixin):

    def get_object_data(self, pk=None):
        if pk is None:
            pk = self.pk

        try:
            return self.queryset().get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFoundError()

    def put_object_data(self, obj, data):
        with transaction.atomic():
            self.save_object(obj, data)

    def delete_object_data(self, obj):
        obj.delete()
