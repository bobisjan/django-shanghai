from django.utils.module_loading import autodiscover_modules

from shanghai.apps import Shanghai


def autodiscover():
    """
    Automatically discover `resources` modules in `INSTALLED_APPS`.
    """

    autodiscover_modules('resources', register_to=api)


default_app_config = 'shanghai.apps.ShanghaiConfig'


# Register a globally available instance of the Shanghai application.
api = Shanghai()
