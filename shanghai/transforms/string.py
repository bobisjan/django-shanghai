from .base import Transform


class StringTransform(Transform):

    def serialize(self, deserialized):
        if deserialized:
            return str(deserialized)

    def deserialize(self, serialized):
        if serialized:
            return str(serialized)
