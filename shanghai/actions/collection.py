from django.db import transaction


class CollectionMixin(object):

    def get_collection_data(self):
        return self.get_queryset()

    def get_collection(self):
        data = self.get_collection_data()

        return self.response(data)

    def get_collection_input_data(self):
        return self.input.get(self.type)

    def post_collection(self):
        data = self.get_collection_input_data()

        if isinstance(data, dict):
            obj = self.model(**data)

            obj.save()
            return self.response(obj, status=201)
        else:
            objects = list()

            with transaction.atomic():
                for item in data:
                    obj = self.model(**item)

                    obj.save()
                    objects.append(obj)

            return self.response(objects, status=201)
