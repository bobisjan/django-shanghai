import sys

from django.conf import settings
from django.http import HttpResponseServerError

from shanghai.http import HttpResponseNotImplemented
from shanghai.utils import is_iterable, setattrs


class DispatcherMixin(object):

    @staticmethod
    def action_not_resolved():
        return HttpResponseServerError()

    @staticmethod
    def action_not_implemented():
        return HttpResponseNotImplemented()

    @staticmethod
    def resolve_pk(pk):
        if pk is None or not len(pk):
            return None

        parts = pk.split(',')
        if len(parts) > 1:
            pk = parts
        return pk

    def resolve_parameters(self):
        pk = self.kwargs.get('pk', None)
        link = self.kwargs.get('link', None)
        link_pk = self.kwargs.get('link_pk', None)

        pk = self.resolve_pk(pk)
        link_pk = self.resolve_pk(link_pk)
        return pk, link, link_pk

    def resolve_action(self):
        method = self.request.method.lower()

        if self.pk is None:
            return method, 'collection'
        elif self.link is None:
            if isinstance(self.pk, str):
                return method, 'object'
            elif is_iterable(self.pk):
                return method, 'objects'
        elif self.link_pk is None:
            return method, 'linked'
        elif isinstance(self.link_pk, str):
            return method, 'linked_object'
        elif is_iterable(self.link_pk):
            return method, 'linked_objects'

    def resolve_input(self):
        import json

        method = self.request.method.lower()

        if method in ('post', 'put'):
            body = self.request.body
            return json.loads(body.decode(settings.DEFAULT_CHARSET))

    def dispatch(self, request, *args, **kwargs):
        setattrs(self, request=request, args=args, kwargs=kwargs)

        pk, link, link_pk = self.resolve_parameters()
        setattrs(self, pk=pk, link=link, link_pk=link_pk)

        action = self.resolve_action()
        setattr(self, 'action', action)

        if not action:
            return self.action_not_resolved()

        input = self.resolve_input()
        setattr(self, 'input', input)

        callback = getattr(self, '_'.join(action), self.action_not_implemented)

        try:
            response = callback()
        except:
            exc_info = sys.exc_info()

            if settings.DEBUG:
                raise

            return self.response_with_error(exc_info[1])
        else:
            return response
