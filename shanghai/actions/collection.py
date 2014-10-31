from django.db import transaction


class CollectionMixin(object):

    def get_collection_data(self):
        raise NotImplementedError()

    def get_collection(self):
        data = self.get_collection_data()

        return self.response(data)

    def get_collection_input_data(self):
        return self.input.get(self.type)

    def post_collection(self):
        data = self.get_collection_input_data()

        object_or_iterable = self.post_collection_data(data)

        return self.response(object_or_iterable, status=201)

    def post_collection_data(self, data):
        raise NotImplementedError()


class ModelCollectionMixin(CollectionMixin):

    def get_collection_data(self):
        return self.get_queryset()

    def post_collection_data(self, data):
        if isinstance(data, dict):
            obj = self.model(**data)

            obj.save()

            return obj
        else:
            objects = list()

            with transaction.atomic():
                for item in data:
                    obj = self.model(**item)

                    obj.save()
                    objects.append(obj)

            return objects
