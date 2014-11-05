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
