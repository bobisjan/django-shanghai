from .boolean import BooleanTransform
from .date import DateTransform, DateTimeTransform, TimeTransform
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
register_transform('time', TimeTransform)
register_transform('float', FloatTransform)
register_transform('integer', IntegerTransform)
register_transform('decimal', DecimalTransform)
register_transform('string', StringTransform)
