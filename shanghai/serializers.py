import inflection

from shanghai.exceptions import ForbiddenError
from shanghai.utils import is_iterable


class Serializer(object):
    """
    A JSONAPI serializer.
    """

    def __init__(self, resource):
        self.resource = resource

    def serialize(self, object_or_iterable, links=None, **kwargs):
        document = dict()

        document['data'] = self.serialize_object_or_iterable(object_or_iterable)

        if links:
            document['links'] = links

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

        self.serialize_id(obj, data, self.resource.primary_key())
        self.serialize_type(obj, data)

        attributes = self.resource.attributes()
        for key in attributes.keys():
            self.serialize_attribute(obj, data, attributes.get(key))

        self.serialize_self_link(obj, data, self.links_for_data(data))

        relationships = self.resource.get_relationships()
        for key in relationships.keys():
            self.serialize_relationship(obj, data, relationships.get(key))

        return data

    def serialize_id(self, obj, data, pk):
        key = self.key_for_id(pk)
        value = self.resource.fetch_id(obj, pk)
        value = self.normalize_id(value)
        data[key] = value

    def serialize_type(self, obj, data):
        data['type'] = self.key_for_type(self.resource.type)

    def serialize_self_link(self, obj, data, links, link=None, related=None):
        primary_key = self.resource.primary_key()
        key = self.key_for_id(primary_key)
        pk = data[key]

        if related:
            related = self.key_for_relationship(related)
            links['resource'] = self.resource.absolute_reverse_url(pk=pk, related=related)
        elif link:
            link = self.key_for_relationship(link)
            links['self'] = self.resource.absolute_reverse_url(pk=pk, link=link)
        else:
            links['self'] = self.resource.absolute_reverse_url(pk=pk)

    @staticmethod
    def normalize_id(value):
        return str(value)

    def serialize_attribute(self, obj, data, attribute):
        key = self.key_for_attribute(attribute)
        value = self.resource.fetch_attribute(obj, attribute)
        value = attribute.transform.serialize(value)
        data[key] = value

    def serialize_relationship(self, obj, data, relationship):
        resource = self.resource_for_relationship(relationship)
        links = self.links_for_data(data)
        link = None

        if relationship.is_has_many():
            target = resource.fetch_has_many(obj, relationship)
            link = self.link_for_has_many(obj, data, target, resource, relationship)
        elif relationship.is_belongs_to():
            target = resource.fetch_belongs_to(obj, relationship)
            link = self.link_for_belongs_to(obj, data, target, resource, relationship)

        key = self.key_for_relationship(relationship)
        links[key] = link

    def link_for_belongs_to(self, obj, data, related, resource, relationship):
        if not related:
            return None

        primary_key = resource.primary_key()
        pk = resource.fetch_id(related, primary_key)

        link = dict(
            type=self.key_for_type(resource.type),
            id=self.normalize_id(pk)
        )

        self.serialize_self_link(obj, data, link, link=relationship)
        self.serialize_self_link(obj, data, link, related=relationship)

        return link

    def link_for_has_many(self, obj, data, related, resource, relationship):
        primary_key = resource.primary_key()
        pks = list()

        for obj in related:
            pk = primary_key.get_from(obj)
            pk = self.normalize_id(pk)
            pks.append(pk)

        link = dict(
            type=self.key_for_type(resource.type),
            ids=pks
        )

        self.serialize_self_link(obj, data, link, link=relationship)
        self.serialize_self_link(obj, data, link, related=relationship)

        return link

    def links_for_data(self, data):
        if 'links' not in data:
            data['links'] = dict()
        return data.get('links')

    def resource_for_relationship(self, relationship):
        return self.resource.api.resource_for(relationship.target)

    def key_for_type(self, name):
        return inflection.dasherize(name)

    def key_for_id(self, pk):
        return inflection.dasherize(pk.name)

    def key_for_attribute(self, attribute):
        return inflection.dasherize(attribute.name)

    def key_for_relationship(self, relationship):
        return inflection.dasherize(relationship.name)

    def extract(self, document):
        object_or_iterable = document.get('data')

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

        primary_key = self.resource.primary_key()
        self.extract_id(obj, data, primary_key)

        self.extract_type(obj, data)

        attributes = self.resource.attributes()
        for attribute in attributes.values():
            self.extract_attribute(obj, data, attribute)

        if 'links' in data:
            data_links = data.get('links')
            links = dict()

            relationships = self.resource.get_relationships()
            for relationship in relationships.values():
                self.extract_relationship(links, data_links, relationship)

            if len(links):
                obj['links'] = links

        return obj

    def extract_id(self, obj, data, pk):
        key = self.key_for_id(pk)
        value = data.get(key, None)

        if value:
            obj[pk.name] = pk.transform.deserialize(value)

    def extract_type(self, obj, data):
        if 'type' not in data:
            raise ForbiddenError('Data does not contain `type`.')

        obj['type'] = data['type']

    def extract_attribute(self, obj, data, attribute):
        key = self.key_for_attribute(attribute)

        if key not in data:
            return

        value = data.get(key)
        value = attribute.transform.deserialize(value)

        obj[attribute.name] = value

    def extract_relationship(self, obj, data, relationship):
        resource = self.resource_for_relationship(relationship)
        key = self.key_for_relationship(relationship)
        primary_key = resource.primary_key()

        if key not in data:
            return

        value = data.get(key)

        if 'id' in value and value['id']:
            value['id'] = primary_key.transform.deserialize(value['id'])
        elif 'ids' in value and value['ids']:
            value['ids'] = list(map(primary_key.transform.deserialize, value['ids']))

        obj[relationship.name] = value
