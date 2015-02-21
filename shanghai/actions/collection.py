from django.db import transaction

from shanghai.exceptions import TypeConflictError


class CollectionMixin(object):

    def get_collection(self):
        order_by = self.sort_parameters()
        pagination = self.pagination_parameters()

        data = self.get_collection_data(
            order_by=order_by,
            pagination=pagination
        )

        links = dict()

        if pagination:
            total = self.collection_total()
            self.add_pagination_links(links, pagination, total)

        return self.response(data, links=links)

    def get_collection_data(self, order_by=None):
        raise NotImplementedError()

    def collection_total():
        raise NotImplementedError()

    def collection_input_data(self):
        return self.serializer.extract(self.input)

    def post_collection(self):
        data = self.collection_input_data()

        if self.type != data.get('type'):
            raise TypeConflictError(self.type, data.get('type'))

        obj = self.post_collection_object(data)

        return self.response_with_location(obj)

    def post_collection_object(self, data):
        raise NotImplementedError()


class ModelCollectionMixin(CollectionMixin):

    def get_collection_data(self, order_by=None, pagination=None):
        qs = self.queryset()

        if len(order_by):
            qs = self.sort_queryset(qs, *order_by)

        if pagination:
            qs = self.limit_queryset(qs, pagination)

        return qs

    def collection_total(self):
        return self.queryset().count()

    def post_collection_object(self, data):
        with transaction.atomic():
            return self.save_object(self.create_object(), data)
