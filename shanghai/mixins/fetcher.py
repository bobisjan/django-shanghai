from django.core.exceptions import ObjectDoesNotExist

from shanghai.exceptions import NotFoundError


class FetcherMixin(object):

    def fetch_id(self, obj, primary_key=None):
        primary_key = primary_key or self.primary_key()
        return primary_key.get_from(obj)

    def fetch_attribute(self, obj, attribute):
        return attribute.get_from(obj)

    def fetch_belongs_to(self, obj, relationship):
        return relationship.get_from(obj)

    def fetch_has_many(self, obj, relationship):
        return relationship.get_from(obj)

    def fetch_collection(self):
        raise NotImplementedError()

    def fetch_object(self, pk=None):
        raise NotImplementedError()


class ModelFetcherMixin(FetcherMixin):

    def fetch_has_many(self, obj, relationship):
        related_manager = super(ModelFetcherMixin, self).fetch_has_many(obj, relationship)

        return related_manager.all()

    def fetch_collection(self):
        return self.queryset()

    def fetch_object(self, pk=None):
        if pk is None:
            pk = self.pk

        try:
            return self.queryset().get(pk=pk)
        except ObjectDoesNotExist:
            raise NotFoundError()
