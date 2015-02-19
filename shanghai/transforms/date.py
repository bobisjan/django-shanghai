from django.utils.dateparse import parse_date, parse_datetime, parse_time

from .base import Transform


class DateTransform(Transform):

    def serialize(self, deserialized):
        if not deserialized:
            return deserialized

        return deserialized.isoformat()

    def deserialize(self, serialized):
        if not serialized:
            return serialized

        return parse_date(serialized)


class DateTimeTransform(Transform):

    def serialize(self, deserialized):
        if not deserialized:
            return deserialized

        return deserialized.isoformat()

    def deserialize(self, serialized):
        if not serialized:
            return serialized

        return parse_datetime(serialized)


class TimeTransform(Transform):

    def serialize(self, deserialized):
        if not deserialized:
            return deserialized

        return deserialized.isoformat()

    def deserialize(self, serialized):
        if not serialized:
            return serialized

        return parse_time(serialized)
