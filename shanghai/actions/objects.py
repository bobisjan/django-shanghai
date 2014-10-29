from shanghai.http import HttpResponseNoContent


class ObjectsMixin(object):

    def get_objects_data(self):
        qs = self.get_queryset()

        return qs.filter(pk__in=self.pk)

    def get_objects(self):
        data = self.get_objects_data()

        return self.response(data)

    def delete_objects(self):
        data = self.get_objects_data()

        data.delete()
        return HttpResponseNoContent()
