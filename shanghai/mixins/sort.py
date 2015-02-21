class SortMixin(object):

    def sort_parameters(self):
        order_by = self.request.GET.get('sort', None)

        if order_by is None:
            return list()

        return order_by.split(',')


class ModelSortMixin(SortMixin):

    def sort_parameters(self):
        params = super(ModelSortMixin, self).sort_parameters()

        return list(map(self._normalize_sort, params))

    def sort_queryset(self, qs, *order_by):
        return qs.order_by(*order_by)

    @staticmethod
    def _normalize_sort(sort):
        if sort.startswith('+'):
            return sort[1:]
        return sort
