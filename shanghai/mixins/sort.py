import inflection


class SortMixin(object):

    def sort_parameters(self):
        order_by = self.request.GET.get('sort', None)

        if order_by is None:
            return list()

        params = order_by.split(',')

        return list(map(self.normalize_sort_parameter, params))

    def sort_collection(self, collection, *order_by):
        raise NotImplementedError()

    def normalize_sort_parameter(self, param):
        return param


class ModelSortMixin(SortMixin):

    def sort_collection(self, collection, *order_by):
        return collection.order_by(*order_by)

    def normalize_sort_parameter(self, param):
        sign = param[0]
        param = param[1:]

        param = param.replace('.', '__')
        param = inflection.underscore(param)

        if sign == '+':
            return param
        return sign + param
