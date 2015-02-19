from .boolean import BooleanTransform
from .date import DateTransform, DateTimeTransform, TimeTransform
from .file import FileTransform
from .number import DecimalTransform, FloatTransform, IntegerTransform
from .string import StringTransform


_transforms = {}


def register_transform(name, transform):
    _transforms[name] = transform()


def transform_for(name):
    return _transforms[name]


register_transform('boolean', BooleanTransform)
register_transform('date', DateTransform)
register_transform('datetime', DateTimeTransform)
register_transform('decimal', DecimalTransform)
register_transform('file', FileTransform)
register_transform('float', FloatTransform)
register_transform('integer', IntegerTransform)
register_transform('string', StringTransform)
register_transform('time', TimeTransform)
