from django.utils.module_loading import autodiscover_modules

from shanghai.apps import Shanghai


CONTENT_TYPE = 'application/vnd.api+json'


def autodiscover():
    """
    Automatically discovers `resources` modules in `INSTALLED_APPS`.
    """

    autodiscover_modules('resources', register_to=api)


def autoinspect():
    """
    Automatically inspects registered resources.
    """

    api.inspect()


default_app_config = 'shanghai.apps.ShanghaiConfig'


# Register a globally available instance of the Shanghai application.
api = Shanghai()
