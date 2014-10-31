class FetcherMixin(object):

    def fetch_id(self, obj, id):
        return id.get_from(obj)

    def fetch_attribute(self, obj, attribute):
        return attribute.get_from(obj)

    def fetch_belongs_to(self, obj, relationship):
        return relationship.get_from(obj)

    def fetch_has_many(self, obj, relationship):
        return relationship.get_from(obj)


class ModelFetcherMixin(FetcherMixin):

    def fetch_has_many(self, obj, relationship):
        related_manager = super(ModelFetcherMixin, self).fetch_has_many(obj, relationship)

        return related_manager.all()
