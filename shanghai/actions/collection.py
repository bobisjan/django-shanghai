from django.db import transaction

from shanghai.exceptions import TypeConflictError


class CollectionMixin(object):

    def get_collection(self):
        data = self.get_collection_data()

        return self.response(data)

    def get_collection_data(self):
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

    def get_collection_data(self):
        return self.queryset()

    def post_collection_object(self, data):
        with transaction.atomic():
            return self.save_object(self.create_object(), data)
