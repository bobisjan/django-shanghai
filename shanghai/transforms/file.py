from .base import Transform


class FileTransform(Transform):

    def serialize(self, deserialized):
        return getattr(deserialized, 'url', None)
