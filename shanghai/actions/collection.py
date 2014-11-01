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

    def _post_collection_object(self, data):
        links = dict()

        if 'links' in data:
            links = data.get('links')
            del data['links']

        obj = self.model(**data)

        for key in links.keys():
            relationship = self.relationship_for(key)
            linked_resource = self.get_linked_resource(relationship)
            linked_pk = links.get(key)

            if relationship.is_belongs_to():
                linked_obj = None

                if linked_pk:
                    linked_obj = linked_resource.get_object_data(linked_pk)

                    if not linked_obj:
                        raise RuntimeError()

                relationship.set_to(obj, linked_obj)

        obj.save()

        for key in links.keys():
            relationship = self.relationship_for(key)
            linked_resource = self.get_linked_resource(relationship)
            linked_pk = links.get(key)

            if relationship.is_has_many():
                linked_objects = list()

                if len(linked_pk):
                    linked_objects = linked_resource.get_objects_data(linked_pk)

                    if len(linked_pk) != len(linked_objects):
                        raise RuntimeError()

                relationship.set_to(obj, linked_objects)

        return obj

    def post_collection_object(self, data):
        with transaction.atomic():
            return self._post_collection_object(data)

    def post_collection_objects(self, data):
        objects = list()

        with transaction.atomic():
            for item in data:
                obj = self._post_collection_object(item)

                objects.append(obj)

        return objects

