import shanghai
from shanghai.actions import *
from shanghai.inspectors import Inspector, MetaInspector, ModelInspector
from shanghai.mixins import *
from shanghai.serializers import Serializer


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

    def url_pattern_name(self, *args):
        return '-'.join([self.api.name, self.name] + list(args))

    def generate_urls(self):
        from django.conf.urls import patterns, url

        view = self.dispatch
        pk = '\w+([,]?(\w+))*'
        link = '\w+'

        url_patterns = patterns('',
            url(r'^{0}/(?P<pk>{1})/links/(?P<link>{2})/(?P<link_pk>{1})'.format(self.type, pk, link), view, name=self.url_pattern_name('pk', 'link', 'link-pk')),
            url(r'^{0}/(?P<pk>{1})/links/(?P<link>{2})'.format(self.type, pk, link), view, name=self.url_pattern_name('pk', 'link')),
            url(r'^{0}/(?P<pk>{1})'.format(self.type, pk), view, name=self.url_pattern_name('pk')),
            url(r'^{0}'.format(self.type), view, name=self.url_pattern_name()),
        )

        return url_patterns

    def reverse_url(self, pk=None, link=None, link_pk=None):
        from django.core.urlresolvers import reverse

        pattern_args = list()
        reverse_args = list()

        if pk:
            pattern_args.append('pk')
            reverse_args.append(pk)

        if link:
            pattern_args.append('link')
            reverse_args.append(link)

        if link_pk:
            pattern_args.append('link-pk')
            reverse_args.append(link_pk)

        name = self.url_pattern_name(*pattern_args)
        url = reverse(name, args=reverse_args)

        return url.replace('%2C', ',')

    @property
    def urls(self):
        return self.generate_urls()

    def __str__(self):
        return self.name


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
