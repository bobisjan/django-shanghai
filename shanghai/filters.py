import inflection

from shanghai.exceptions import ForbiddenError
from shanghai.properties import Id, Attribute, Relationship
from shanghai.transforms import transform_for


_filters = dict()


def register_filter(suffix, filter):
    _filters[suffix] = filter


def filter_for(resource, path):
    parts = path.split(Filter.SUFFIX_DELIMITER)
    key = parts[0]
    suffix = None

    if len(parts) == 2:
        suffix = parts[1]

    if suffix is None:
        return Filter(resource, key)

    suffix = inflection.underscore(suffix)

    if suffix not in _filters:
        raise ForbiddenError('Unknown filter suffix `{0}` for key `{1}`.'.format(suffix, key))

    filter = _filters[suffix]
    return filter(resource, key)


class Filter(object):

    SUFFIX_DELIMITER = ':'
    PATH_DELIMITER = '.'

    suffix = None

    def __init__(self, resource, key):
        self.resource = resource
        self.key = key
        self.property = self._detect_property()

    @property
    def path(self):
        if self.suffix is None:
            return self.key

        return self.SUFFIX_DELIMITER.join([self.key, self.suffix])

    def _detect_property(self):
        parts = self.key.split(self.PATH_DELIMITER)
        resource = self.resource

        for part in parts:
            property = resource.property_for(part)

            if isinstance(property, Id) or isinstance(property, Attribute):
                return property

            if isinstance(property, Relationship):
                resource = resource.api.resource_for(property.target)
                continue

        raise ForbiddenError('Unknown property for key {0} on resource {1}'.format(self.key, self.resource))

    def normalize_value(self, value):
        transform = self.property.transform

        return transform.deserialize(value)


class ExactFilter(Filter):

    suffix = 'exact'


class IExactFilter(Filter):

    suffix = 'iexact'


class ContainsFilter(Filter):

    suffix = 'contains'


class IContainsFilter(Filter):

    suffix = 'icontains'


class InFilter(Filter):

    ITEMS_DELIMITER = ','

    suffix = 'in'

    def normalize_value(self, value):
        items = value.split(self.ITEMS_DELIMITER)

        return list(map(super(InFilter, self).normalize_value, items))


class RangeFilter(Filter):

    ITEMS_DELIMITER = ','

    suffix = 'range'

    def normalize_value(self, value):
        items = value.split(self.ITEMS_DELIMITER)

        if len(items) != 2:
            raise ForbiddenError('Range filter accepts only start and end values.')

        return list(map(super(RangeFilter, self).normalize_value, items))


class GreaterThenFilter(Filter):

    suffix = 'gt'


class GreaterThenEqualFilter(Filter):

    suffix = 'gte'


class LowerThenFilter(Filter):

    suffix = 'lt'


class LowerThenEqualFilter(Filter):

    suffix = 'lte'


class StartsWithFilter(Filter):

    suffix = 'startswith'


class IStartsWithFilter(Filter):

    suffix = 'istartswith'


class EndsWithFilter(Filter):

    suffix = 'endswith'


class IEndsWithFilter(Filter):

    suffix = 'iendswith'


class YearFilter(Filter):

    suffix = 'year'

    def normalize_value(self, value):
        return transform_for('integer').deserialize(value)


class MonthFilter(Filter):

    suffix = 'month'

    def normalize_value(self, value):
        month = transform_for('integer').deserialize(value)

        if month < 1 or month > 12:
            raise ForbiddenError('Month filter accepts only numbers from 1 to 12.')

        return month


class DayFilter(Filter):

    suffix = 'day'

    def normalize_value(self, value):
        day = transform_for('integer').deserialize(value)

        if day < 1 or day > 31:
            raise ForbiddenError('Day filter accepts only numbers from 1 to 31.')

        return day


class WeekDayFilter(Filter):

    suffix = 'week_day'

    def normalize_value(self, value):
        week_day = transform_for('integer').deserialize(value)

        if week_day < 1 or week_day > 7:
            raise ForbiddenError('Week day filter accepts only numbers from 1 to 7.')

        return week_day


class HourFilter(Filter):

    suffix = 'hour'

    def normalize_value(self, value):
        hour = transform_for('integer').deserialize(value)

        if hour < 0 or hour > 23:
            raise ForbiddenError('Hour filter accepts only numbers from 0 to 23.')

        return hour


class MinuteFilter(Filter):

    suffix = 'minute'

    def normalize_value(self, value):
        minute = transform_for('integer').deserialize(value)

        if minute < 0 or minute > 59:
            raise ForbiddenError('Minute filter accepts only numbers from 0 to 59.')

        return minute


class SecondFilter(Filter):

    suffix = 'second'

    def normalize_value(self, value):
        second = transform_for('integer').deserialize(value)

        if second < 0 or second > 59:
            raise ForbiddenError('Second filter accepts only numbers from 0 to 59.')

        return second


class IsNullFilter(Filter):

    suffix = 'isnull'

    def normalize_value(self, value):
        return transform_for('boolean').deserialize(value)


class SearchFilter(Filter):

    suffix = 'search'


class RegexFilter(Filter):

    suffix = 'regex'


class IRegexFilter(Filter):

    suffix = 'iregex'


register_filter(IsNullFilter.suffix, IsNullFilter)
register_filter(ExactFilter.suffix, ExactFilter)
register_filter(IExactFilter.suffix, IExactFilter)
register_filter(ContainsFilter.suffix, ContainsFilter)
register_filter(IContainsFilter.suffix, IContainsFilter)
register_filter(StartsWithFilter.suffix, StartsWithFilter)
register_filter(IStartsWithFilter.suffix, IStartsWithFilter)
register_filter(EndsWithFilter.suffix, EndsWithFilter)
register_filter(IEndsWithFilter.suffix, IEndsWithFilter)
register_filter(RegexFilter.suffix, RegexFilter)
register_filter(IRegexFilter.suffix, IRegexFilter)
register_filter(SearchFilter.suffix, SearchFilter)
register_filter(GreaterThenFilter.suffix, GreaterThenFilter)
register_filter(GreaterThenEqualFilter.suffix, GreaterThenEqualFilter)
register_filter(LowerThenFilter.suffix, LowerThenFilter)
register_filter(LowerThenEqualFilter.suffix, LowerThenEqualFilter)
register_filter(InFilter.suffix, InFilter)
register_filter(RangeFilter.suffix, RangeFilter)
register_filter(YearFilter.suffix, YearFilter)
register_filter(MonthFilter.suffix, MonthFilter)
register_filter(DayFilter.suffix, DayFilter)
register_filter(WeekDayFilter.suffix, WeekDayFilter)
register_filter(HourFilter.suffix, HourFilter)
register_filter(MinuteFilter.suffix, MinuteFilter)
register_filter(SecondFilter.suffix, SecondFilter)
