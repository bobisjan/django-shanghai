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
               FilterMixin, SortMixin, PaginationMixin, LinkerMixin, object):
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

    @property
    def urls(self):
        return self.generate_urls()

    def __str__(self):
        return self.name

    # TODO find a suitable mixin

    def process_collection(self, collection):
        filters = self.filter_parameters()
        sorters = self.sort_parameters()
        pagination = self.pagination_parameters()

        if len(filters):
            collection = self.filter_collection(collection, **filters)

        if len(sorters):
            collection = self.sort_collection(collection, *sorters)

        if pagination:
            pagination['total'] = self.count_collection(collection)
            collection = self.paginate_collection(collection, pagination)

        return collection, dict(filters=filters, sorters=sorters, pagination=pagination)

    def meta_for_document(self, object_or_iterable, **kwargs):
        # TODO `pagination.total`
        return None

    def meta_for_object(self, obj, **kwargs):
        return None


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
        links = data.get('links', dict())
        update_fields = list()

        for key, attribute in self.attributes().items():
            if key not in data:
                continue

            attribute.set_to(obj, data.get(key))
            update_fields.append(key)

        for key, relationship in self.relationships().items():
            if key not in links:
                continue

            linked_resource = self.linked_resource(relationship)
            linkage = links[key]

            if relationship.is_belongs_to():
                linked_obj = None

                if linkage:
                    pk = linkage['id']
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

        for key, relationship in self.relationships().items():
            if key not in links:
                continue

            linked_resource = self.linked_resource(relationship)
            linkage = links[key]

            if relationship.is_has_many():
                related_manager = relationship.get_from(obj)
                pks = [item['id'] for item in linkage]
                linked_objects = list()

                if len(pks):
                    linked_objects = linked_resource._get_objects_data(pks)

                relationship.set_to(obj, linked_objects)

        return obj

    def remove_object(self, obj):
        obj.delete()
