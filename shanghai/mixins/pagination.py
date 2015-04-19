from shanghai.exceptions import ForbiddenError


class PaginationMixin(object):

    def pagination_parameters(self):
        offset = self.request.GET.get('page[offset]', None)
        limit = self.request.GET.get('page[limit]', None)

        if offset is not None and limit is not None:
            return dict(offset=int(offset), limit=int(limit))
        return None

    def paginate_collection(self, collection, pagination):
        raise NotImplementedError()

    def is_offset_limit_strategy(self, pagination):
        return 'offset' in pagination and 'limit' in pagination

    def count_collection(self, collection):
        raise NotImplementedError()

    def add_pagination_links(self, links, pagination, **kwargs):
        offset = pagination['offset']
        limit = pagination['limit']
        total = pagination['total']

        links['first'] = self.pagination_link(0, limit, **kwargs)

        prev = offset - limit
        if prev >= 0:
            links['prev'] = self.pagination_link(prev, limit, **kwargs)
        else:
            links['prev'] = None

        next = offset + limit
        if next < total:
            links['next'] = self.pagination_link(next, limit, **kwargs)
        else:
            links['next'] = None

        last = (total - (total % limit))
        if last < 0 or total == limit:
            last = 0
        links['last'] = self.pagination_link(last, limit, **kwargs)

    def pagination_link(self, offset, limit, **kwargs):
        url = self.absolute_reverse_url(**kwargs)
        # TODO refactor
        offset = 'page[offset]=' + str(offset)
        limit = 'page[limit]=' + str(limit)
        return url + '?' + '&'.join([offset, limit])


class ModelPaginationMixin(PaginationMixin):

    def pagination_parameters(self):
        pagination = super(ModelPaginationMixin, self).pagination_parameters()

        if not pagination:
            return None

        if not self.is_offset_limit_strategy(pagination):
            raise ForbiddenError('Unsupported pagination strategy')
        return pagination

    def paginate_collection(self, collection, pagination):
        offset = pagination['offset']
        limit = pagination['limit']
        return collection[offset:offset+limit]

    def count_collection(self, collection):
        return collection.count()
