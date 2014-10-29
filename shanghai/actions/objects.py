from shanghai.http import HttpResponseNoContent


class ObjectsMixin(object):

    def get_objects_data(self, pk=None):
        qs = self.get_queryset()

        if not pk:
            pk = self.pk

        return qs.filter(pk__in=pk)

    def get_objects(self):
        data = self.get_objects_data()

        return self.response(data)

    def delete_objects(self):
        data = self.get_objects_data()

        data.delete()
        return HttpResponseNoContent()
