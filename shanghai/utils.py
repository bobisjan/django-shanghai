from django.db import models

import shanghai


def setattrs(obj, **kwargs):
    for attr in kwargs.keys():
        setattr(obj, attr, kwargs.get(attr))


def is_iterable(object_or_iterable):
    """
    Tests if passed argument is iterable or not.

    :param object_or_iterable: Instance to test
    :return: True if argument is iterable, otherwise False
    """

    try:
        iter(object_or_iterable)
        return True
    except TypeError:
        return False


def resource_for_model(model, api=shanghai.api):
    resources = getattr(api, '_registry')

    for resource in resources.values():
        current = getattr(resource, 'model', None)

        if model is current:
            return resource


field_to_kind = {
    'django.db.models.fields.AutoField': 'integer',
    'django.db.models.fields.related.OneToOneField': 'integer',
    'django.db.models.fields.BooleanField': 'boolean',
    'django.db.models.fields.DecimalField': 'decimal',
    'django.db.models.fields.SmallIntegerField': 'integer',
    'django.db.models.fields.PositiveSmallIntegerField': 'integer',
    'django.db.models.fields.IntegerField': 'integer',
    'django.db.models.fields.PositiveIntegerField': 'integer',
    'django.db.models.fields.BigIntegerField': 'integer',
    'django.db.models.fields.FloatField': 'float',
    'django.db.models.fields.CharField': 'string',
    'django.db.models.fields.SlugField': 'string',
    'django.db.models.fields.TextField': 'string',
    'django.db.models.fields.URLField': 'string',
    'django.db.models.fields.EmailField': 'string',
    'django.db.models.fields.FilePathField': 'string',
    'django.db.models.fields.DateField': 'date',
    'django.db.models.fields.DateTimeField': 'datetime',
    'django.db.models.fields.TimeField': 'time',
    'django.db.models.fields.FileField': 'file',
    'django.db.models.fields.ImageField': 'file',
}


def kind_of_field(field):
    path = field.__module__ + '.' + type(field).__name__

    return field_to_kind.get(path, None)
