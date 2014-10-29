from django.http import HttpResponseNotFound
from django.db import models


class ObjectMixin(object):

    def get_object_data(self):
        qs = self.get_queryset()

        try:
            obj = qs.get(pk=self.pk)
        except models.ObjectDoesNotExist:
            return None
        else:
            return obj

    def get_object(self):
        data = self.get_object_data()

        if not data:
            return HttpResponseNotFound()
        return self.response(data)
