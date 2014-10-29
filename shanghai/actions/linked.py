from django.http import HttpResponseNotFound
from django.db import models

from shanghai.http import HttpResponseNoContent


class LinkedMixin(object):

    def get_linked_data(self):
        qs = self.get_queryset()

        try:
            obj = qs.get(pk=self.pk)
        except models.ObjectDoesNotExist:
            return None
        else:
            relationship = self.get_linked_relationship()

            return relationship.get_from(obj)

    def get_linked_serializer(self):
        relationship = self.get_linked_relationship()
        resource = self.api.resource_for(relationship.target)

        return resource.serializer

    def get_linked_relationship(self):
        return self.relationship_for(self.link)

    def get_linked(self):
        data = self.get_linked_data()

        if not data:
            return HttpResponseNotFound()

        serializer = self.get_linked_serializer()
        return self.response(data, serializer=serializer)

    def delete_linked(self):
        obj = self.get_object_data()
        relationship = self.get_linked_relationship()

        if not obj or not relationship.is_belongs_to():
            return HttpResponseNotFound()

        relationship.set_to(obj, None)
        update_fields = [relationship.name]
        obj.save(update_fields=update_fields)
        return HttpResponseNoContent()


class LinkedObjectMixin(object):
    pass


class LinkedObjectsMixin(object):
    pass
