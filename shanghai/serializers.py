import inflection

from shanghai.exceptions import ForbiddenError
from shanghai.utils import is_iterable


class Serializer(object):
    """
    A JSONAPI serializer.
    """

    def __init__(self, resource):
        self.resource = resource

    def serialize(self, object_or_iterable, parent=None, linked=None, related=None, **kwargs):
        document = dict()

        meta = self.serialize_document_meta(object_or_iterable, **kwargs)
        if meta and len(meta):
            document['meta'] = meta

        links = self.serialize_document_links(object_or_iterable, parent, linked=linked, related=related, **kwargs)
        if links and len(links):
            document['links'] = links

        data = self.serialize_primary_data(object_or_iterable, linked=linked, **kwargs)
        document['data'] = data

        included = self.serialize_included(object_or_iterable, **kwargs)
        if included and len(included):
            document['included'] = included

        return document

    def serialize_document_meta(self, object_or_iterable, **kwargs):
        return self.resource.meta_for_document(object_or_iterable, **kwargs)

    def serialize_object_meta(self, obj, **kwargs):
        return self.resource.meta_for_object(obj, **kwargs)

    def serialize_document_links(self, object_or_iterable, parent=None, linked=None, related=None, **kwargs):
        resource = parent or self.resource
        return resource.links_for_document(object_or_iterable, linked=linked, related=related, **kwargs)

    def serialize_object_links(self, obj, **kwargs):
        return self.resource.links_for_object(obj, **kwargs)

    def serialize_primary_data(self, object_or_iterable, linked=None, **kwargs):
        if linked:
            return self.serialize_linked(object_or_iterable, linked)

        if is_iterable(object_or_iterable):
            return self.serialize_collection(object_or_iterable, **kwargs)
        elif object_or_iterable:
            return self.serialize_object(object_or_iterable, **kwargs)

    def serialize_included(self, object_or_iterable, **kwargs):
        return None

    def serialize_collection(self, collection, **kwargs):
        return [self.serialize_object(obj, **kwargs) for obj in collection]

    def serialize_object(self, obj, **kwargs):
        data = dict()

        self.serialize_id(obj, data, self.resource.primary_key())
        self.serialize_type(obj, data)

        attributes = self.resource.attributes()
        for key in attributes.keys():
            self.serialize_attribute(obj, data, attributes.get(key))

        meta = self.serialize_object_meta(obj, **kwargs)
        if meta and len(meta):
            data['meta'] = meta

        data['links'] = self.serialize_object_links(obj, **kwargs)

        relationships = self.resource.relationships()
        for key in relationships.keys():
            self.serialize_relationship(obj, data, relationships.get(key), **kwargs)

        return data

    def serialize_id(self, obj, data, primary_key):
        key = self.key_for_primary_key(primary_key.name)
        value = self.resource.fetch_id(obj, primary_key)
        value = primary_key.transform.serialize(value)
        value = self.normalize_id(value)
        data[key] = value

    def serialize_type(self, obj, data):
        data['type'] = self.key_for_type(self.resource.type)

    def serialize_attribute(self, obj, data, attribute):
        key = self.key_for_attribute(attribute.name)
        value = self.resource.fetch_attribute(obj, attribute)
        value = attribute.transform.serialize(value)
        data[key] = value

    def serialize_relationship(self, obj, data, relationship, **kwargs):
        kwargs.setdefault('pk', data['id'])
        link_object = self.resource.links_for_linked(obj, relationship, **kwargs)
        links = data.setdefault('links', dict())

        link_object['linkage'] = self.serialize_linked(obj, relationship, fetch=True)

        key = self.key_for_relationship(relationship.name)
        links[key] = link_object

    def serialize_linked(self, obj, relationship, fetch=False):
        resource = self.resource_for_relationship(relationship)

        target = obj
        if fetch:
            if relationship.is_has_many():
                target = resource.fetch_has_many(obj, relationship)
            elif relationship.is_belongs_to():
                target = resource.fetch_belongs_to(obj, relationship)

        if relationship.is_has_many():
            return [self.linkage_object(item, resource) for item in target]
        elif relationship.is_belongs_to():
            return self.linkage_object(target, resource)

    def linkage_object(self, obj, resource):
        if not obj:
            return None

        resource_type = self.key_for_type(resource.type)
        primary_key = resource.primary_key()

        pk = primary_key.get_from(obj)
        pk = primary_key.transform.serialize(pk)
        pk = self.normalize_id(pk)

        return dict(type=resource_type, id=pk)

    def resource_for_relationship(self, relationship):
        return self.resource.api.resource_for(relationship.target)

    def extract(self, document):
        object_or_iterable = document.get('data')
        return self.extract_object_or_iterable(object_or_iterable)

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

            relationships = self.resource.relationships()
            for relationship in relationships.values():
                self.extract_relationship(links, data_links, relationship)

            if len(links):
                obj['links'] = links

        return obj

    def extract_id(self, obj, data, primary_key):
        key = self.key_for_primary_key(primary_key.name)
        value = data.get(key, None)

        if value:
            obj[primary_key.name] = primary_key.transform.deserialize(value)

    def extract_type(self, obj, data):
        if 'type' not in data:
            raise ForbiddenError('Data does not contain `type`.')
        obj['type'] = data['type']

    def extract_attribute(self, obj, data, attribute):
        key = self.key_for_attribute(attribute.name)

        if key not in data:
            return

        value = data[key]
        value = attribute.transform.deserialize(value)

        obj[attribute.name] = value

    def extract_relationship(self, obj, data, relationship):
        key = self.key_for_relationship(relationship.name)

        if key not in data:
            return

        resource = self.resource_for_relationship(relationship)
        primary_key = resource.primary_key()
        transform = primary_key.transform
        linkage = data[key]['linkage']

        if relationship.is_belongs_to():
            linkage['id'] = transform.deserialize(linkage['id'])
        elif relationship.is_has_many():
            for item in linkage:
                item['id'] = transform.deserialize(item['id'])

        obj[relationship.name] = linkage

    @staticmethod
    def normalize_id(value):
        return str(value)

    def key_for_primary_key(self, key):
        return inflection.dasherize(key)

    def key_for_type(self, key):
        return inflection.dasherize(key)

    def key_for_attribute(self, key):
        return inflection.dasherize(key)

    def key_for_relationship(self, key):
        return inflection.dasherize(key)
