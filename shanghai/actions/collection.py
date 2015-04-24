from django.db import transaction

from shanghai.exceptions import TypeConflictError


class CollectionMixin(object):

    def get_collection(self):
        collection = self.fetch_collection()
        collection, params = self.process_collection(collection)
        return self.response(collection, **params)

    def post_collection(self):
        data = self.resolve_collection_input()

        if self.type != data['type']:
            raise TypeConflictError(self.type, data['type'])

        obj = self.post_collection_object(data)
        return self.response(obj)

    def post_collection_object(self, data):
        raise NotImplementedError()

    def resolve_collection_input(self):
        return self.serializer.extract(self.input)


class ModelCollectionMixin(CollectionMixin):

    def post_collection_object(self, data):
        with transaction.atomic():
            return self.save_object(self.create_object(), data)
