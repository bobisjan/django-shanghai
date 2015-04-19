import sys

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from shanghai.http import HttpResponseNotImplemented
from shanghai.utils import setattrs


class DispatcherMixin(object):

    def action_not_implemented(self):
        return HttpResponseNotImplemented()

    def resolve_pk(self, pk):
        return self.primary_key().transform.deserialize(pk)

    def resolve_parameters(self):
        pk = self.kwargs.get('pk', None)
        link = self.kwargs.get('link', None)
        related = self.kwargs.get('related', None)

        pk = self.resolve_pk(pk)

        return pk, link, related

    def resolve_action(self):
        method = self.request.method.lower()

        if self.pk is None:
            return method, 'collection'
        elif self.link:
            return method, 'linked'
        elif self.related:
            return method, 'related'
        else:
            return method, 'object'

    def resolve_input(self):
        import json

        method = self.request.method.lower()
        body = self.request.body

        if method in ('post', 'patch', 'delete') and body is not None:
            body = body.decode(settings.DEFAULT_CHARSET)

            if body is None or not len(body):
                return None

            return json.loads(body)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        setattrs(self, request=request, args=args, kwargs=kwargs)

        pk, link, related = self.resolve_parameters()
        setattrs(self, pk=pk, link=link, related=related)

        action = self.resolve_action()
        setattr(self, 'action', action)

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
