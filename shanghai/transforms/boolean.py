from .base import Transform


class BooleanTransform(Transform):

    def serialize(self, deserialized):
        if deserialized is None:
            return deserialized

        return bool(deserialized)

    def deserialize(self, serialized):
        if serialized is None:
            return serialized

        if isinstance(serialized, bool):
            return serialized
        elif isinstance(serialized, str):
            if serialized in ('t', 'true', 'True', '1'):
                return True
            elif serialized in ('f', 'false', 'False', '0'):
                return False
        elif isinstance(serialized, int):
            return serialized == 1
        else:
            return False
