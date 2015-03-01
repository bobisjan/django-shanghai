from shanghai.exceptions import ForbiddenError
from shanghai.http import HttpResponseNoContent


class LinkedMixin(object):

    def linked_relationship(self):
        return self.relationship_for(self.link)

    def linked_resource(self, relationship=None):
        if not relationship:
            relationship = self.linked_relationship()

        return self.api.resource_for(relationship.target)

    def resolve_linked_input(self):
        return self.input.get('data')

    def post_linked(self):
        obj = self.fetch_object()
        relationship = self.linked_relationship()

        if not relationship.is_has_many():
            raise ForbiddenError()

        self.post_linked_has_many(obj, relationship)

        return HttpResponseNoContent()

    def post_linked_has_many(self, obj, relationship):
        raise NotImplementedError()

    def put_linked(self):
        obj = self.fetch_object()
        relationship = self.linked_relationship()
        linked_resource = self.linked_resource()
        linked_data = self.resolve_linked_input()

        if relationship.is_belongs_to():
            self.put_linked_belongs_to(obj, relationship, linked_resource, linked_data)
        elif relationship.is_has_many():
            self.put_linked_has_many(obj, relationship, linked_resource, linked_data)
        else:
            raise ForbiddenError()

        return HttpResponseNoContent()

    def put_linked_belongs_to(self, obj, relationship, linked_resource, linked_data):
        raise NotImplementedError()

    def put_linked_has_many(self, obj, relationship, linked_resource, linked_data):
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

    def post_linked_has_many(self, obj, relationship):
        related_manager = relationship.get_from(obj)
        linked_data = self.resolve_linked_input()
        linked_resource = self.linked_resource()

        pks = linked_data.get('ids')  # TODO extract ids via serializer

        count = related_manager.all().filter(pk__in=pks).count()
        if count > 0:
            raise ForbiddenError()

        linked_objects = linked_resource._get_objects_data(pks)
        related_manager.add(*linked_objects)

    def put_linked_belongs_to(self, obj, relationship, linked_resource, linked_data):
        linked_obj = None

        if linked_data:
            pk = linked_data.get('id')  # TODO extract id via serializer
            linked_obj = linked_resource.fetch_object(pk)

        relationship.set_to(obj, linked_obj)
        obj.save(update_fields=[relationship.name])

    def put_linked_has_many(self, obj, relationship, linked_resource, linked_data):
        linked_objects = list()
        pks = linked_data.get('ids')  # TODO extract ids via serializer

        if len(pks):
            linked_objects = linked_resource._get_objects_data(pks)

        relationship.set_to(obj, linked_objects)

    def delete_linked_has_many(self, obj, data, relationship):
        related_manager = relationship.get_from(obj)
        resource = self.linked_resource()
        pks = data.get('ids')  # TODO extract ids via serializer
        linked_objects = resource._get_objects_data(pks)

        related_manager.remove(*linked_objects)
