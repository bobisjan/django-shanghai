from shanghai.exceptions import ForbiddenError
from shanghai.http import HttpResponseNoContent


class LinkedMixin(object):

    def get_linked(self):
        relationship = self.linked_relationship()
        obj = self.fetch_object()

        if relationship.is_belongs_to():
            return self.get_linked_belongs_to(obj, relationship)
        elif relationship.is_has_many():
            return self.get_linked_has_many(obj, relationship)

    def get_linked_belongs_to(self, obj, relationship):
        raise NotImplementedError()

    def get_linked_has_many(self, obj, relationship):
        raise NotImplementedError()

    def post_linked(self):
        obj = self.fetch_object()
        relationship = self.linked_relationship()

        if not relationship.is_has_many():
            raise ForbiddenError()

        self.post_linked_has_many(obj, relationship)
        return HttpResponseNoContent()

    def post_linked_has_many(self, obj, relationship):
        raise NotImplementedError()

    def patch_linked(self):
        obj = self.fetch_object()
        relationship = self.linked_relationship()
        resource = self.linked_resource()
        data = self.resolve_linked_input()

        if relationship.is_belongs_to():
            self.patch_linked_belongs_to(obj, relationship, resource, data)
        elif relationship.is_has_many():
            self.patch_linked_has_many(obj, relationship, resource, data)

        return HttpResponseNoContent()

    def linked_serializer(self):
        resource = self.linked_resource()
        return resource.serializer

    def linked_relationship(self):
        return self.relationship_for(self.link)

    def linked_resource(self, relationship=None):
        if not relationship:
            relationship = self.linked_relationship()

        resource = self.api.resource_for(relationship.target)
        setattr(resource, 'request', self.request)
        return resource

    def resolve_linked_input(self):
        return self.input.get('data')

    def patch_linked_belongs_to(self, obj, relationship, resource, data):
        raise NotImplementedError()

    def patch_linked_has_many(self, obj, relationship, resource, data):
        raise NotImplementedError()

    def delete_linked(self):
        obj = self.fetch_object()
        data = self.resolve_linked_input()
        relationship = self.linked_relationship()

        if not relationship.is_has_many():
            raise ForbiddenError()

        self.delete_linked_has_many(obj, data, relationship)
        return HttpResponseNoContent()

    def delete_linked_has_many(self, obj, data, relationship):
        raise NotImplementedError()


class ModelLinkedMixin(LinkedMixin):

    def get_linked_belongs_to(self, obj, relationship):
        serializer = self.linked_serializer()
        data = relationship.get_from(obj)
        return self.response(data, serializer=serializer, parent=self, linked=relationship)

    def get_linked_has_many(self, obj, relationship):
        serializer = self.linked_serializer()
        collection = self.fetch_has_many(obj, relationship)
        collection, params = self.process_collection(collection)
        return self.response(collection, serializer=serializer, parent=self, linked=relationship, **params)

    def post_linked_has_many(self, obj, relationship):
        related_manager = relationship.get_from(obj)
        data = self.resolve_linked_input()
        resource = self.linked_resource()

        pks = data['ids']

        count = related_manager.all().filter(pk__in=pks).count()
        if count > 0:
            raise ForbiddenError()

        linked_objects = resource._get_objects_data(pks)
        related_manager.add(*linked_objects)

    def patch_linked_belongs_to(self, obj, relationship, resource, data):
        linked_obj = None

        if data:
            pk = data['id']
            linked_obj = resource.fetch_object(pk)

        relationship.set_to(obj, linked_obj)
        obj.save(update_fields=[relationship.name])

    def patch_linked_has_many(self, obj, relationship, resource, data):
        linked_objects = list()
        pks = data['ids']

        if len(pks):
            linked_objects = resource._get_objects_data(pks)

        relationship.set_to(obj, linked_objects)

    def delete_linked_has_many(self, obj, data, relationship):
        related_manager = relationship.get_from(obj)
        resource = self.linked_resource()
        pks = data['ids']
        linked_objects = resource._get_objects_data(pks)

        related_manager.remove(*linked_objects)
