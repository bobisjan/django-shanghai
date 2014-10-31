from django.conf import settings
from django.http import HttpResponseServerError

import shanghai
from shanghai.actions import *
from shanghai.http import HttpResponseNotImplemented, JsonApiResponse
from shanghai.inspectors import Inspector, MetaInspector, ModelInspector
from shanghai.serializers import Serializer
from shanghai.utils import is_iterable, setattrs


class MetaMixin(object):

    def get_id(self):
        return getattr(self, 'id')

    def get_attributes(self):
        return getattr(self, 'attributes')

    def attribute_for(self, name):
        attributes = self.get_attributes()

        return attributes.get(name)

    def get_relationships(self):
        return getattr(self, 'relationships')

    def relationship_for(self, name):
        relationships = self.get_relationships()

        return relationships.get(name)


class FetcherMixin(object):

    def fetch_id(self, obj, id):
        return id.get_from(obj)

    def fetch_attribute(self, obj, attribute):
        return attribute.get_from(obj)

    def fetch_belongs_to(self, obj, relationship):
        return relationship.get_from(obj)

    def fetch_has_many(self, obj, relationship):
        return relationship.get_from(obj)


class ModelFetcherMixin(FetcherMixin):

    def fetch_has_many(self, obj, relationship):
        related_manager = super(ModelFetcherMixin, self).fetch_has_many(obj, relationship)

        return related_manager.all()


class ResponderMixin(object):

    def response(self, data, serializer=None, **kwargs):
        if not serializer:
            serializer = getattr(self, 'serializer')

        serialized_data = serializer.serialize(data)
        return JsonApiResponse(serialized_data, **kwargs)


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
        return callback()


class Resource(CollectionMixin, ObjectMixin, ObjectsMixin,
               LinkedMixin, LinkedObjectMixin, LinkedObjectsMixin,
               FetcherMixin, MetaMixin, ResponderMixin, DispatcherMixin, object):
    """
    A base class for all resources.
    """

    inspector = MetaInspector

    serializer = Serializer

    def __init__(self, api=shanghai.api):
        self.api = api

        self.name = self.resolve_name()
        self.type = self.resolve_type()

        self.inspector = self.resolve_inspector()
        self.serializer = self.resolve_serializer()

        # generic request attributes
        self.request = None
        self.args = None
        self.kwargs = None

        # resolved action attributes
        self.action = None
        self.pk = None
        self.link = None
        self.link_pk = None

        self.input = None

    def resolve_name(self):
        # TODO resolve from class name if not specified
        return getattr(type(self), 'name')

    def resolve_type(self):
        # TODO dasherize
        return self.name.replace('_', '-')

    def resolve_inspector(self):
        inspector = getattr(type(self), 'inspector', Inspector)

        return inspector(self)

    def resolve_serializer(self):
        serializer = getattr(type(self), 'serializer', Serializer)

        return serializer(self)

    def generate_urls(self):
        from django.conf.urls import patterns, url

        view = self.dispatch
        pk = '\w+([,]?(\w+))*'
        link = '\w+'

        url_patterns = patterns('',
            url(r'^{0}/(?P<pk>{1})/links/(?P<link>{2})/(?P<link_pk>{1})'.format(self.type, pk, link), view),
            url(r'^{0}/(?P<pk>{1})/links/(?P<link>{2})'.format(self.type, pk, link), view),
            url(r'^{0}/(?P<pk>{1})'.format(self.type, pk), view),
            url(r'^{0}'.format(self.type), view),
        )

        return url_patterns

    @property
    def urls(self):
        return self.generate_urls()


class ModelResource(ModelCollectionMixin, ModelObjectMixin, ModelObjectsMixin,
                    ModelLinkedMixin, ModelLinkedObjectMixin, ModelLinkedObjectsMixin,
                    ModelFetcherMixin, Resource):
    """
    A model based resource.
    """

    model = None

    inspector = ModelInspector

    def get_queryset(self):
        return self.model.objects.all()
