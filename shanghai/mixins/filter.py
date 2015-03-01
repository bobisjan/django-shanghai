import inflection

from shanghai.filters import filter_for


class FilterMixin(object):

    def filter_collection(self, collection, **filters):
        raise NotImplementedError()

    def filter_parameters(self):
        filters = dict()

        for key, value in self.request.GET.items():
            if not key.startswith('filter'):
                continue

            _key = key[len('filter['):-1]
            filter = filter_for(self.filter_resource(), _key)

            _key = self.normalize_filter_key(filter, _key)
            _value = self.normalize_filter_value(filter, value)
            filters[_key] = _value

        return filters

    def filter_resource(self):
        if self.related is not None:
            return self.related_resource()

        return self

    def normalize_filter_key(self, filter, key):
        return filter.path

    def normalize_filter_value(self, filter, value):
        return filter.normalize_value(value)


class ModelFilterMixin(FilterMixin):

    def filter_collection(self, collection, **kwargs):
        return collection.filter(**kwargs)

    def normalize_filter_key(self, filter, key):
        key = super(ModelFilterMixin, self).normalize_filter_key(filter, key)

        key = key.replace(filter.SUFFIX_DELIMITER, '__')
        key = key.replace(filter.PATH_DELIMITER, '__')
        key = inflection.underscore(key)

        return key
