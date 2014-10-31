from django.db import transaction

from shanghai.http import HttpResponseNoContent


class ObjectsMixin(object):

    def get_objects_data(self, pk=None):
        raise NotImplementedError()

    def get_objects_input_data(self):
        return self.input.get(self.type)

    def get_objects(self):
        data = self.get_objects_data()

        return self.response(data)

    def put_objects(self):
        data = self.get_objects_input_data()

        return self.put_objects_data(data)

    def put_objects_data(self, data):
        raise NotImplementedError()

    def delete_objects(self):
        data = self.get_objects_data()

        return self.delete_objects_data(data)

    def delete_objects_data(self, data):
        raise NotImplementedError()


class ModelObjectsMixin(ObjectsMixin):

    def get_objects_data(self, pk=None):
        qs = self.get_queryset()

        if not pk:
            pk = self.pk

        return qs.filter(pk__in=pk)

    def put_objects_data(self, data):
        with transaction.atomic():
            for item in data:
                _id = self.get_id()
                pk = item.get(_id.name)

                obj = self.get_object_data(pk=pk)
                self._put_object(obj, item)

        return HttpResponseNoContent()

    def delete_objects_data(self, data):
        data.delete()

        return HttpResponseNoContent()
