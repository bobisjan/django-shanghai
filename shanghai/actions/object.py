from django.http import HttpResponseNotFound
from django.db import models

from shanghai.http import HttpResponseNoContent


class ObjectMixin(object):

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

        self._put_object(obj, data)
        return HttpResponseNoContent()

    def _put_object(self, obj, data):
        update_fields = list()

        if not obj:
            return HttpResponseNotFound()

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
                        continue

                update_fields.append(key)
                relationship.set_to(obj, linked_obj)
            elif relationship.is_has_many():
                linked_objects = list()

                if len(linked_pk):
                    linked_objects = linked_resource.get_objects_data(pk=linked_pk)

                relationship.set_to(obj, linked_objects)

        obj.save(update_fields=update_fields)

    def delete_object(self):
        data = self.get_object_data()

        if not data:
            return HttpResponseNotFound()

        data.delete()
        return HttpResponseNoContent()
