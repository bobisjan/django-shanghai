import inflection


class FieldsMixin(object):

    fields = dict()

    related_fields = dict()

    def get_fields(self):
        return self.fields

    def get_related_fields(self):
        return self.related_fields

    def get_fieldsets(self, related=None):
        fields = dict()

        if related:
            related_fields = self.get_related_fields()
            if related.name in related_fields:
                fields = related_fields[related.name]
        else:
            fields = self.get_fields()

        fields = self.fields_parameters() or fields

        fieldsets = dict()
        for key, value in fields.items():
            resource = self.api.resource_for(key)
            properties = set()

            if not resource:
                continue  # TODO raise?

            for item in value:
                prop = resource.property_for(item)

                if not prop:
                    continue  # TODO raise?
                properties.add(prop)

            fieldsets[resource] = properties

        return fieldsets

    def fields_parameters(self):
        fields = dict()

        for key, value in self.request.GET.items():
            if not key.startswith('fields'):
                continue

            _key = key[len('fields['):-1]
            _key = self.normalize_fields_key(_key)

            _value = value.split(',')
            _value = list(map(self.normalize_fields_value, _value))

            fields[_key] = _value

        return fields

    def normalize_fields_key(self, key):
        return inflection.underscore(key)

    def normalize_fields_value(self, value):
        return inflection.underscore(value)
