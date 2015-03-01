from django.core.exceptions import ValidationError

import inflection

import shanghai
from shanghai.actions import *
from shanghai.exceptions import ModelValidationError, NotFoundError
from shanghai.inspectors import Inspector, MetaInspector, ModelInspector
from shanghai.mixins import *
from shanghai.serializers import Serializer


class Resource(CollectionMixin, ObjectMixin, LinkedMixin, RelatedMixin,
               FetcherMixin, MetaMixin, ResponderMixin, DispatcherMixin,
               FilterMixin, SortMixin, PaginationMixin, object):
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
        self.related = None

        self.input = None

    def resolve_name(self):
        cls = type(self)
        name = getattr(cls, 'name', None)

        if name is None:
            name = cls.__name__[:-len('Resource')]
            name = inflection.underscore(name)
            name = inflection.pluralize(name)

        return name

    def resolve_type(self):
        return inflection.dasherize(self.name)

    def resolve_inspector(self):
        inspector = getattr(type(self), 'inspector', Inspector)

        return inspector(self)

    def resolve_serializer(self):
        serializer = getattr(type(self), 'serializer', Serializer)

        return serializer(self)

    def url_pattern_name(self, *args):
        return '-'.join([self.api.name, self.type] + list(args))

    def generate_urls(self):
        from django.conf.urls import patterns, url

        view = self.dispatch
        pk = '\w+([,]?(\w+))*'
        link = related = '\w+'

        url_patterns = patterns('',
            url(r'^{0}/(?P<pk>{1})/links/(?P<link>{2})'.format(self.type, pk, link), view, name=self.url_pattern_name('pk', 'link')),
            url(r'^{0}/(?P<pk>{1})/(?P<related>{2})'.format(self.type, pk, related), view, name=self.url_pattern_name('pk', 'related')),
            url(r'^{0}/(?P<pk>{1})'.format(self.type, pk), view, name=self.url_pattern_name('pk')),
            url(r'^{0}'.format(self.type), view, name=self.url_pattern_name()),
        )

        return url_patterns

    def reverse_url(self, pk=None, link=None, related=None):
        from django.core.urlresolvers import reverse

        pattern_args = list()
        reverse_args = list()

        if pk:
            pattern_args.append('pk')
            reverse_args.append(pk)

        if link:
            pattern_args.append('link')
            reverse_args.append(link)

        if related:
            pattern_args.append('related')
            reverse_args.append(related)

        name = self.url_pattern_name(*pattern_args)
        url = reverse(name, args=reverse_args)

        return url.replace('%2C', ',')

    def absolute_reverse_url(self, pk=None, link=None, related=None):
        return self.request.build_absolute_uri(self.reverse_url(pk, link, related))

    @property
    def urls(self):
        return self.generate_urls()

    def __str__(self):
        return self.name


class ModelResource(ModelCollectionMixin, ModelObjectMixin,
                    ModelLinkedMixin, ModelRelatedMixin, ModelFetcherMixin,
                    ModelFilterMixin, ModelSortMixin, ModelPaginationMixin,
                    Resource):
    """
    A model based resource.
    """

    model = None

    inspector = ModelInspector

    def queryset(self):
        return self.model.objects.all()

    def _get_objects_data(self, pks):
        if not pks or not len(pks):
            return list()

        objects = self.queryset().filter(pk__in=pks)

        if len(pks) != len(objects):
            raise NotFoundError()

        return objects

    def create_object(self):
        return self.model()

    def save_object(self, obj, data):
        pk, attributes, links = self.serializer.unpack(data)
        update_fields = list()

        for key, value in attributes.items():
            setattr(obj, key, value)
            update_fields.append(key)

        for key, linked_data in links.items():
            relationship = self.relationship_for(key)
            linked_resource = self.linked_resource(relationship)

            if relationship.is_belongs_to():
                linked_obj = None

                if linked_data:
                    pk = linked_data.get('id')  # TODO extract id via serializer
                    linked_obj = linked_resource.fetch_object(pk)

                relationship.set_to(obj, linked_obj)
                update_fields.append(key)

        try:
            obj.full_clean()
        except ValidationError as error:
            raise ModelValidationError(error)

        if obj.pk:
            obj.save(update_fields=update_fields)
        else:
            obj.save()

        for key, linked_data in links.items():
            relationship = self.relationship_for(key)
            resource = self.linked_resource(relationship)

            if relationship.is_has_many():
                related_manager = relationship.get_from(obj)
                pks = linked_data.get('ids')  # TODO extract ids via serializer
                linked_objects = list()

                if len(pks):
                    linked_objects = resource._get_objects_data(pks)

                relationship.set_to(obj, linked_objects)

        return obj
