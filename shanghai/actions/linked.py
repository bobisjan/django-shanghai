from django.http import HttpResponseNotFound

from shanghai.exceptions import LinkedResourceAlreadyExists
from shanghai.http import HttpResponseNoContent


class LinkedMixin(object):

    def get_linked_relationship(self):
        return self.relationship_for(self.link)

    def get_linked_resource(self, relationship=None):
        if not relationship:
            relationship = self.get_linked_relationship()

        return self.api.resource_for(relationship.target)

    def get_linked_serializer(self):
        resource = self.get_linked_resource()

        return resource.serializer

    def get_linked_data(self):
        raise NotImplementedError()

    def get_linked_input_data(self):
        relationship = self.get_linked_relationship()
        return self.input.get(relationship.target)

    def get_linked(self):
        data = self.get_linked_data()
        serializer = self.get_linked_serializer()

        return self.response(data, serializer=serializer)

    def post_linked(self):
        obj = self.get_object_data()
        relationship = self.get_linked_relationship()

        self.post_linked_data(obj, relationship)

        return HttpResponseNoContent()

    def post_linked_data(self, obj, relationship):
        raise NotImplementedError()

    def put_linked(self):
        obj = self.get_object_data()
        relationship = self.get_linked_relationship()
        linked_resource = self.get_linked_resource()
        linked_pk = self.get_linked_input_data()

        self.put_linked_data(obj, relationship, linked_resource, linked_pk)

        return HttpResponseNoContent()

    def put_linked_data(self, obj, relationship, linked_resource, linked_pk):
        raise NotImplementedError()

    def delete_linked(self):
        obj = self.get_object_data()
        relationship = self.get_linked_relationship()

        if not relationship.is_belongs_to():
            return HttpResponseNotFound()

        self.delete_linked_data(obj, relationship)

        return HttpResponseNoContent()

    def delete_linked_data(self, obj, relationship):
        raise NotImplementedError()


class ModelLinkedMixin(LinkedMixin):

    def get_linked_data(self):
        obj = self.get_object_data()
        relationship = self.get_linked_relationship()

        if relationship.is_belongs_to():
            return relationship.get_from(obj)
        elif relationship.is_has_many():
            related_manager = relationship.get_from(obj)

            return related_manager.all()

    def post_linked_data(self, obj, relationship):
        if relationship.is_belongs_to():
            link = self.get_linked_data()
            if link:
                raise LinkedResourceAlreadyExists(self, obj, relationship, link)

            linked_pk = self.get_linked_input_data()
            linked_resource = self.get_linked_resource()
            linked_object = linked_resource.get_object_data(linked_pk)

            relationship.set_to(obj, linked_object)
            obj.save()
        elif relationship.is_has_many():
            related_manager = relationship.get_from(obj)

            if related_manager.count():
                raise LinkedResourceAlreadyExists(self, obj, relationship, related_manager.all())

            linked_pk = self.get_linked_input_data()
            linked_resource = self.get_linked_resource()

            if isinstance(linked_pk, str):
                linked_pk = linked_pk,

            linked_objects = linked_resource.get_objects_data(linked_pk)
            related_manager.add(*linked_objects)

    def put_linked_data(self, obj, relationship, linked_resource, linked_pk):
        if relationship.is_belongs_to():
            linked_obj = None

            if linked_pk:
                linked_obj = linked_resource.get_object_data(linked_pk)

            relationship.set_to(obj, linked_obj)
            obj.save(update_fields=[relationship.name])

        elif relationship.is_has_many():
            linked_objects = list()

            if len(linked_pk):
                linked_objects = linked_resource.get_objects_data(linked_pk)

            relationship.set_to(obj, linked_objects)

    def delete_linked_data(self, obj, relationship):
        relationship.set_to(obj, None)
        update_fields = [relationship.name]
        obj.save(update_fields=update_fields)
