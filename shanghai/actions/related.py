from shanghai.exceptions import ForbiddenError


class RelatedMixin(object):

    def get_related(self):
        relationship = self.related_relationship()
        obj = self.fetch_object()

        if relationship.is_belongs_to():
            return self.get_related_belongs_to(obj, relationship)
        elif relationship.is_has_many():
            return self.get_related_has_many(obj, relationship)

    def get_related_belongs_to(self, obj, relationship):
        raise NotImplementedError()

    def get_related_has_many(self, obj, relationship):
        raise NotImplementedError()

    def related_serializer(self):
        resource = self.related_resource()
        return resource.serializer

    def related_relationship(self):
        return self.relationship_for(self.related)

    def related_resource(self, relationship=None):
        if not relationship:
            relationship = self.related_relationship()

        resource = self.api.resource_for(relationship.target)
        setattr(resource, 'request', self.request)
        return resource


class ModelRelatedMixin(RelatedMixin):

    def get_related_belongs_to(self, obj, relationship):
        serializer = self.related_serializer()
        data = relationship.get_from(obj)
        return self.response(data, serializer=serializer, parent=self, related=relationship)

    def get_related_has_many(self, obj, relationship):
        serializer = self.related_serializer()
        collection = self.fetch_has_many(obj, relationship)
        collection, params = self.process_collection(collection)
        return self.response(collection, serializer=serializer, parent=self, related=relationship, **params)
