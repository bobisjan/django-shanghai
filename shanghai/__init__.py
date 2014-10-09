from django.utils.module_loading import autodiscover_modules


def autodiscover():
    """
    Automatically discover `resources` modules in `INSTALLED_APPS`.
    """

    autodiscover_modules('resources', register_to=api)


class Shanghai(object):
    """
    A main class for a Shanghai application.
    """

    def __init__(self):
        self._registry = {}


default_app_config = 'shanghai.apps.ShanghaiConfig'


# Register a globally available instance of the Shanghai application.
api = Shanghai()
