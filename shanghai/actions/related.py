class RelatedMixin(object):

    def get_related(self):
        data = self.get_related_data()
        serializer = self.related_serializer()

        return self.response(data, serializer=serializer)

    def get_related_data(self):
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

    def get_related_data(self):
        obj = self.get_object_data()
        relationship = self.related_relationship()

        if relationship.is_belongs_to():
            return relationship.get_from(obj)

        elif relationship.is_has_many():
            related_manager = relationship.get_from(obj)
            qs = related_manager.all()

            order_by = self.sort_parameters()
            if len(order_by):
                qs = self.sort_queryset(qs, *order_by)

            return qs
