from django.http import HttpResponseNotFound
from django.db import models


class LinkedMixin(object):

    def get_linked_data(self):
        qs = self.get_queryset()

        try:
            obj = qs.get(pk=self.pk)
        except models.ObjectDoesNotExist:
            return None
        else:
            relationship = self.relationship_for(self.link)

            return relationship.get_from(obj)

    def get_linked_serializer(self):
        relationship = self.relationship_for(self.link)
        resource = self.api.resource_for(relationship.target)

        return resource.serializer

    def get_linked(self):
        data = self.get_linked_data()

        if not data:
            return HttpResponseNotFound()

        serializer = self.get_linked_serializer()
        return self.response(data, serializer=serializer)


class LinkedObjectMixin(object):
    pass


class LinkedObjectsMixin(object):
    pass
