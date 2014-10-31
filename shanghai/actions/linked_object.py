from django.http import HttpResponseNotFound

from shanghai.http import HttpResponseNoContent


class LinkedObjectMixin(object):

    def get_linked_object_data(self):
        resource = self.get_linked_resource()

        return resource.get_object_data(self.link_pk)

    def delete_linked_object(self):
        obj = self.get_object_data()
        relationship = self.get_linked_relationship()
        data = relationship.get_from(obj)
        linked_object = self.get_linked_object_data()

        if not obj or not relationship.is_has_many():
            return HttpResponseNotFound()

        self.delete_linked_object_data(data, linked_object)

        return HttpResponseNoContent()

    def delete_linked_object_data(self, data):
        raise NotImplementedError()


class ModelLinkedObjectMixin(LinkedObjectMixin):

    def delete_linked_object_data(self, data, linked_object):
        data.remove(linked_object)
