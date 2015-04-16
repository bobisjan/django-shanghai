from shanghai.exceptions import ForbiddenError


class RelatedMixin(object):

    def get_related(self):
        relationship = self.related_relationship()
        obj = self.fetch_object()

        if relationship.is_belongs_to():
            return self.get_related_belongs_to(obj, relationship)
        elif relationship.is_has_many():
            return self.get_related_has_many(obj, relationship)
        else:
            raise ForbiddenError()

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

        return self.response(data, serializer=serializer)

    def get_related_has_many(self, obj, relationship):
        collection = self.fetch_has_many(obj, relationship)
        serializer = self.related_serializer()
        links = dict()

        filters = self.filter_parameters()
        if len(filters):
            collection = self.filter_collection(collection, **filters)

        order_by = self.sort_parameters()
        if len(order_by):
            collection = self.sort_collection(collection, *order_by)

        pagination = self.pagination_parameters()
        if pagination:
            total = self.count_collection(collection)
            collection = self.paginate_collection(collection, pagination)
            self.add_pagination_links(links, pagination, total, pk=self.pk, related=self.related)

        return self.response(collection, serializer=serializer, links=links)
