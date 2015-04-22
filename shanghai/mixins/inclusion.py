import inflection

from shanghai.utils import is_iterable


class InclusionMixin(object):

    include = []

    related_include = {}

    def get_include(self, related=None):
        include = []

        if not related:
            include = self.include
        elif related.name in self.related_include:
            include = self.related_include[related.name]

        return self.include_parameters() or include

    def include_parameters(self):
        include = self.request.GET.get('include', None)

        if include is None:
            return list()

        parameters = include.split(',')
        return list(map(self.normalize_include_parameter, parameters))

    def normalize_include_parameter(self, key):
        key = key.replace('.', '__')
        return inflection.underscore(key)

    def included_for(self, obj_or_iterable, parent=None, related=None, **kwargs):
        if not is_iterable(obj_or_iterable):
            obj_or_iterable = [obj_or_iterable]

        pks = [self.fetch_id(obj) for obj in obj_or_iterable]

        include = self.get_include(related=related)
        includes = dict()

        for path in include:
            relationships = self.reverse_relationship_path(path, parent)
            resource = self.api.resource_for(relationships[0].target)
            collection = resource.fetch_collection()
            included_filter = self.included_filter(relationships, pks)

            included = resource.filter_collection(collection, **included_filter)

            objects = includes.setdefault(resource, set())
            includes[resource] = objects.union(set(included))

        result = list()
        for resource, items in includes.items():
            resource.request = self.request or parent.request
            result.extend([(resource, item) for item in items])
        return result

    def included_filter(self, relationships, pks):
        parts = list()
        for item in relationships:
            resource = self.api.resource_for(item.target)
            relationship = resource.relationship_for(item.inverse)
            parts.append(relationship.attr_name)

        path = '__'.join(parts + ['in'])

        f = dict()
        f[path] = pks
        return f

    def reverse_relationship_path(self, path, parent=None):
        resource = parent or self
        parts = path.split('__')
        relationships = []

        for part in parts:
            relationship = resource.relationship_for(part)
            relationships.append(relationship)
            resource = relationship.target

        relationships.reverse()
        return relationships
