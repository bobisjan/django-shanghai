from django.db import transaction

from shanghai.exceptions import TypeConflictError


class CollectionMixin(object):

    def get_collection(self):
        filters = self.filter_parameters()
        order_by = self.sort_parameters()
        pagination = self.pagination_parameters()

        collection = self.fetch_collection()
        links = dict()

        if len(filters):
            collection = self.filter_collection(collection, **filters)

        if len(order_by):
            collection = self.sort_collection(collection, *order_by)

        if pagination:
            total = self.count_collection(collection)
            collection = self.paginate_collection(collection, pagination)
            self.add_pagination_links(links, pagination, total)

        return self.response(collection, links=links)

    def post_collection(self):
        data = self.resolve_collection_input()

        if self.type != data.get('type'):
            raise TypeConflictError(self.type, data.get('type'))

        obj = self.post_collection_object(data)

        return self.response_with_location(obj)

    def post_collection_object(self, data):
        raise NotImplementedError()

    def resolve_collection_input(self):
        return self.serializer.extract(self.input)


class ModelCollectionMixin(CollectionMixin):

    def post_collection_object(self, data):
        with transaction.atomic():
            return self.save_object(self.create_object(), data)
