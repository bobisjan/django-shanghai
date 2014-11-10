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


def kind_of_field(field):
    from django.db import models

    if isinstance(field, models.BooleanField):
        return 'boolean'

    if isinstance(field, models.DecimalField):
        return 'decimal'

    if isinstance(field, (models.SmallIntegerField, models.PositiveSmallIntegerField, models.IntegerField,
                          models.PositiveIntegerField, models.BigIntegerField)):
        return 'integer'

    if isinstance(field, models.FloatField):
        return 'float'

    if isinstance(field, (models.CharField, models.SlugField, models.TextField, models.URLField, models.EmailField)):
        return 'string'

    if isinstance(field, models.DateField):
        return 'date'

    if isinstance(field, models.DateTimeField):
        return 'datetime'

    if isinstance(field, models.TimeField):
        return 'time'
