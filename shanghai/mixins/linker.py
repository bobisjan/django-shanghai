from shanghai.utils import is_iterable


class LinkerMixin(object):

    def links_for_document(self, object_or_iterable, linked=None, related=None, **kwargs):
        if linked:
            return self.links_for_linked(object_or_iterable, linked, **kwargs)

        if related:
            return self.links_for_related(object_or_iterable, related, **kwargs)

        if is_iterable(object_or_iterable):
            return self.links_for_collection(object_or_iterable, **kwargs)
        else:
            return self.links_for_object(object_or_iterable, **kwargs)

    def links_for_object(self, obj, **kwargs):
        links = dict()

        pk = self.fetch_id(obj, self.primary_key())
        links['self'] = self.absolute_reverse_url(pk=pk)

        return links

    def links_for_collection(self, collection, **kwargs):
        links = dict()
        links['self'] = self.absolute_reverse_url()

        pagination = kwargs.get('pagination', None)
        if pagination:
            pkwargs = dict()
            if self.pk and self.related:
                pkwargs['pk'] = self.pk
                pkwargs['related'] = self.related
            self.add_pagination_links(links, pagination, **pkwargs)

        return links

    def links_for_related(self, object_or_iterable, relationship, **kwargs):
        links = dict()

        key = self.serializer.key_for_relationship(relationship.name)
        links['self'] = self.absolute_reverse_url(pk=self.pk, related=key)

        if relationship.is_has_many():
            pagination = kwargs.get('pagination', None)
            if pagination:
                pkwargs = dict()
                if self.pk and self.related:
                    pkwargs['pk'] = self.pk
                    pkwargs['related'] = self.related
                self.add_pagination_links(links, pagination, **pkwargs)

        return links

    def links_for_linked(self, object_or_iterable, relationship, **kwargs):
        links = dict()

        pk = kwargs.get('pk', None) or self.pk
        key = self.serializer.key_for_relationship(relationship.name)

        links['self'] = self.absolute_reverse_url(pk=pk, link=key)
        links['related'] = self.absolute_reverse_url(pk=pk, related=key)

        return links

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
        url = self.reverse_url(pk, link, related)
        return self.request.build_absolute_uri(url)
