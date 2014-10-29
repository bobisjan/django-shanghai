from django.http import HttpResponseNotFound
from django.db import models

from shanghai.http import HttpResponseNoContent


class ObjectMixin(object):

    def get_object_data(self, pk=None):
        qs = self.get_queryset()

        if not pk:
            pk = self.pk

        try:
            obj = qs.get(pk=pk)
        except models.ObjectDoesNotExist:
            return None
        else:
            return obj

    def get_object(self):
        data = self.get_object_data()

        if not data:
            return HttpResponseNotFound()
        return self.response(data)

    def delete_object(self):
        data = self.get_object_data()

        if not data:
            return HttpResponseNotFound()

        data.delete()
        return HttpResponseNoContent()
