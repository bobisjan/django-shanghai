from django.db import transaction

from shanghai.http import HttpResponseNoContent


class ObjectsMixin(object):

    def get_objects_data(self, pk=None):
        raise NotImplementedError()

    def get_objects_input_data(self):
        return self.serializer.extract(self.input)

    def get_objects(self):
        data = self.get_objects_data()

        return self.response(data)

    def put_objects(self):
        data = self.get_objects_input_data()

        updated_objects = self.put_objects_data(data)

        if updated_objects:
            return self.response(updated_objects)

        return HttpResponseNoContent()

    def put_objects_data(self, data):
        raise NotImplementedError()

    def delete_objects(self):
        data = self.get_objects_data()

        self.delete_objects_data(data)

        return HttpResponseNoContent()

    def delete_objects_data(self, data):
        raise NotImplementedError()


class ModelObjectsMixin(ObjectsMixin):

    def get_objects_data(self, pk=None):
        qs = self.get_queryset()

        if not pk:
            pk = self.pk

        return qs.filter(pk__in=pk)

    def put_objects_data(self, data):
        updated_objects = list()

        with transaction.atomic():
            for item in data:
                _id = self.get_id()
                pk = item.get(_id.name)

                obj = self.get_object_data(pk)

                if not obj:
                    raise RuntimeError()

                updated_object = self.put_object_data(obj, item)

                if updated_object:
                    updated_objects.append(updated_object)

        if len(updated_objects):
            return updated_objects

    def delete_objects_data(self, data):
        data.delete()
