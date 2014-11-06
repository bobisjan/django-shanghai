from django.db import transaction

from shanghai.http import HttpResponseNoContent


class ObjectMixin(object):

    def get_object_data(self, pk=None):
        raise NotImplementedError()

    def get_object_input_data(self):
        return self.serializer.extract(self.input)

    def get_object(self):
        data = self.get_object_data()

        return self.response(data)

    def put_object(self):
        obj = self.get_object_data()
        data = self.get_object_input_data()

        updated_object = self.put_object_data(obj, data)

        if updated_object:
            return self.response(updated_object)

        return HttpResponseNoContent()

    def put_object_data(self, obj, data):
        raise NotImplementedError()

    def delete_object(self):
        data = self.get_object_data()

        self.delete_object_data(data)

        return HttpResponseNoContent()

    def delete_object_data(self, data):
        raise NotImplementedError()


class ModelObjectMixin(ObjectMixin):

    def get_object_data(self, pk=None):
        qs = self.get_queryset()

        if not pk:
            pk = self.pk

        return qs.get(pk=pk)

    def _put_object_data(self, obj, data):
        pk, attributes, links = self.serializer.unpack(data)
        update_fields = list()

        # update attributes
        for key in attributes.keys():
            update_fields.append(key)
            setattr(obj, key, data.get(key))

        # update `belongs to` relationships
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

        obj.full_clean()
        obj.save(update_fields=update_fields)

        # update `has many` relationships
        for key in links.keys():
            relationship = self.relationship_for(key)
            linked_resource = self.get_linked_resource(relationship)
            linked_pk = links.get(key)

            if relationship.is_has_many():
                linked_objects = list()

                if len(linked_pk):
                    linked_objects = linked_resource.get_objects_data(linked_pk)

                    if len(linked_pk) != len(linked_objects):
                        raise RuntimeError()

                relationship.set_to(obj, linked_objects)

    def put_object_data(self, obj, data):
        with transaction.atomic():
            self._put_object_data(obj, data)

    def delete_object_data(self, data):
        data.delete()
