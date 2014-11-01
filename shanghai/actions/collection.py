from django.db import transaction


class CollectionMixin(object):

    def get_collection_data(self):
        raise NotImplementedError()

    def get_collection(self):
        data = self.get_collection_data()

        return self.response(data)

    def get_collection_input_data(self):
        return self.serializer.extract(self.input)

    def post_collection(self):
        data = self.get_collection_input_data()

        object_or_iterable = self.post_collection_data(data)

        return self.response_with_location(object_or_iterable)

    def post_collection_data(self, data):
        if isinstance(data, list):
            return self.post_collection_objects(data)
        elif isinstance(data, dict):
            return self.post_collection_object(data)
        else:
            raise RuntimeError()

    def post_collection_objects(self, data):
        raise NotImplementedError()

    def post_collection_object(self, data):
        raise NotImplementedError()


class ModelCollectionMixin(CollectionMixin):

    def get_collection_data(self):
        return self.get_queryset()

    def post_collection_object(self, data):
        obj = self.model(**data)

        obj.save()

        return obj

    def post_collection_objects(self, data):
        objects = list()

        with transaction.atomic():
            for item in data:
                obj = self.post_collection_object(item)

                objects.append(obj)

        return objects

