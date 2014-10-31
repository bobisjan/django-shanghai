from django.db import models
from django.http import HttpResponseNotFound

from shanghai.http import HttpResponseNoContent


class ObjectMixin(object):

    def get_object_data(self, pk=None):
        raise NotImplementedError()

    def get_object_input_data(self):
        return self.input.get(self.type)

    def get_object(self):
        data = self.get_object_data()

        if not data:
            return HttpResponseNotFound()

        return self.response(data)

    def put_object(self):
        obj = self.get_object_data()
        data = self.get_object_input_data()

        if not obj:
            return HttpResponseNotFound()

        updated_object = self.put_object_data(obj, data)

        if updated_object:
            return self.response(updated_object)

        return HttpResponseNoContent()

    def put_object_data(self, obj, data):
        raise NotImplementedError()

    def delete_object(self):
        data = self.get_object_data()

        if not data:
            return HttpResponseNotFound()

        self.delete_object_data(data)

        return HttpResponseNoContent()

    def delete_object_data(self, data):
        raise NotImplementedError()


class ModelObjectMixin(ObjectMixin):

    def get_object_data(self, pk=None):
        qs = self.get_queryset()

        if not pk:
            pk = self.pk

        try:
            obj = qs.get(pk=pk)
        except models.ObjectDoesNotExist:
            return None
        else:
            return obj

    def put_object_data(self, obj, data):
        update_fields = list()

        links = dict()
        for key in data.keys():
            if key == self.get_id().name:
                continue

            if key == 'links':
                links = data.get(key)
                continue

            update_fields.append(key)
            setattr(obj, key, data.get(key))

        for key in links.keys():
            relationship = self.relationship_for(key)
            linked_resource = self.get_linked_resource(relationship)
            linked_pk = links.get(key)

            if relationship.is_belongs_to():
                linked_obj = None

                if linked_pk:
                    linked_obj = linked_resource.get_object_data(linked_pk)

                    if not linked_obj:
                        raise RuntimeError()

                update_fields.append(key)
                relationship.set_to(obj, linked_obj)
            elif relationship.is_has_many():
                linked_objects = list()

                if len(linked_pk):
                    linked_objects = linked_resource.get_objects_data(linked_pk)

                relationship.set_to(obj, linked_objects)

        obj.save(update_fields=update_fields)

    def delete_object_data(self, data):
        data.delete()
