from django.http import HttpResponseNotFound

from shanghai.http import HttpResponseNoContent


class LinkedObjectsMixin(object):

    def get_linked_objects_data(self):
        resource = self.get_linked_resource()

        return resource.get_objects_data(self.link_pk)

    def delete_linked_objects(self):
        obj = self.get_object_data()
        relationship = self.get_linked_relationship()
        data = relationship.get_from(obj)
        linked_objects = self.get_linked_objects_data()

        if not relationship.is_has_many():
            return HttpResponseNotFound()

        self.delete_linked_objects_data(data, linked_objects)

        return HttpResponseNoContent()

    def delete_linked_objects_data(self, data, linked_objects):
        raise NotImplementedError()


class ModelLinkedObjectsMixin(LinkedObjectsMixin):

    def delete_linked_objects_data(self, data, linked_objects):
        data.remove(*linked_objects)
