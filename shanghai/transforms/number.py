from decimal import Decimal

from .base import Transform


class DecimalTransform(Transform):

    def serialize(self, deserialized):
        if deserialized:
            return str(deserialized)

    def deserialize(self, serialized):
        if serialized:
            return Decimal(serialized)


class IntegerTransform(Transform):

    def serialize(self, deserialized):
        if deserialized:
            return int(deserialized)

    def deserialize(self, serialized):
        if serialized:
            return int(serialized)


class FloatTransform(Transform):

    def serialize(self, deserialized):
        if deserialized:
            return float(deserialized)

    def deserialize(self, serialized):
        if serialized:
            return float(serialized)
