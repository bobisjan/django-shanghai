from shanghai.utils import is_iterable


class Serializer(object):
    """
    A JSONAPI serializer.
    """

    def __init__(self, resource):
        self.resource = resource

    def serialize(self, object_or_iterable):
        document = dict()

        key = self.key_for_type(self.resource.name)
        document[key] = self.serialize_object_or_iterable(object_or_iterable)

        return document

    def serialize_object_or_iterable(self, object_or_iterable):
        if is_iterable(object_or_iterable):
            return self.serialize_iterable(object_or_iterable)
        elif object_or_iterable:
            return self.serialize_object(object_or_iterable)

    def serialize_iterable(self, objects):
        data = list()

        for obj in objects:
            data.append(self.serialize_object(obj))
        return data

    def serialize_object(self, obj):
        data = dict()

        _id = self.resource.get_id()
        self.serialize_id(obj, data, _id)

        attributes = self.resource.get_attributes()
        for key in attributes.keys():
            self.serialize_attribute(obj, data, attributes.get(key))

        relationships = self.resource.get_relationships()
        for key in relationships.keys():
            self.serialize_relationship(obj, data, relationships.get(key))

        return data

    def serialize_id(self, obj, data, pk):
        key = self.key_for_id(pk)
        value = self.resource.fetch_id(obj, pk)
        value = self.normalize_id(value)
        data[key] = value

    @staticmethod
    def normalize_id(value):
        return str(value)

    def serialize_attribute(self, obj, data, attribute):
        key = self.key_for_attribute(attribute)
        value = self.resource.fetch_attribute(obj, attribute)
        data[key] = value

    def serialize_relationship(self, obj, data, relationship):
        resource = self.resource_for_relationship(relationship)
        links = self.links_for_data(data)
        link = None

        if relationship.is_has_many():
            target = resource.fetch_has_many(obj, relationship)
            link = self.link_for_has_many(target, resource)
        elif relationship.is_belongs_to():
            target = resource.fetch_belongs_to(obj, relationship)
            link = self.link_for_belongs_to(target, resource)

        key = self.key_for_relationship(relationship)
        links[key] = link

    def link_for_belongs_to(self, obj, resource):
        if not obj:
            return None

        _id = resource.get_id()

        pk = resource.fetch_id(obj, _id)

        return self.normalize_id(pk)

    def link_for_has_many(self, objects, resource):
        pk = resource.get_id()
        pks = list()

        for obj in objects:
            _pk = pk.get_from(obj)
            _pk = self.normalize_id(_pk)
            pks.append(_pk)

        return pks

    def links_for_data(self, data):
        if 'links' not in data:
            data['links'] = dict()
        return data.get('links')

    def resource_for_relationship(self, relationship):
        return self.resource.api.resource_for(relationship.target)

    def key_for_type(self, name):
        # TODO camelize
        return name

    def key_for_id(self, pk):
        # TODO camelize
        return pk.name

    def key_for_attribute(self, attribute):
        # TODO camelize
        return attribute.name

    def key_for_relationship(self, relationship):
        # TODO camelize
        return relationship.name

    def extract(self, document):
        key = self.key_for_type(self.resource.name)
        object_or_iterable = document.get(key)

        data = self.extract_object_or_iterable(object_or_iterable)

        return data

    def extract_object_or_iterable(self, object_or_iterable):
        if isinstance(object_or_iterable, list):
            return self.extract_iterable(object_or_iterable)
        elif isinstance(object_or_iterable, dict):
            return self.extract_object(object_or_iterable)

    def extract_iterable(self, data):
        objects = list()

        for item in data:
            objects.append(self.extract_object(item))

        return objects

    def extract_object(self, data):
        obj = dict()

        _id = self.resource.get_id()
        self.extract_id(obj, data, _id)

        attributes = self.resource.get_attributes()
        for key in attributes.keys():
            self.extract_attribute(obj, data, attributes.get(key))

        if 'links' in data:
            data_links = data.get('links')
            links = dict()

            relationships = self.resource.get_relationships()
            for key in relationships.keys():
                self.extract_relationship(links, data_links, relationships.get(key))

            if len(links):
                obj['links'] = links

        return obj

    def extract_id(self, obj, data, pk):
        key = self.key_for_id(pk)

        value = data.get(key, None)

        # TODO de-normalize `id`
        if value:
            obj[pk.name] = value

    def extract_attribute(self, obj, data, attribute):
        key = self.key_for_attribute(attribute)

        if key not in data:
            return

        value = data.get(key)

        obj[attribute.name] = value

    def extract_relationship(self, obj, data, relationship):
        key = self.key_for_relationship(relationship)

        if key not in data:
            return

        value = data.get(key)

        obj[relationship.name] = value

    def unpack(self, data):
        pk = self.unpack_id(data)
        links = dict()

        if 'links' in data:
            links = data.get('links')
            del data['links']

        attributes = data

        return pk, attributes, links

    def unpack_id(self, data):
        id = self.resource.get_id()
        key = self.key_for_id(id)

        pk = None

        if key in data:
            pk = data[key]
            del data[key]

        return pk
