from django.utils.module_loading import autodiscover_modules

from shanghai.conf import settings
from shanghai.apps import Shanghai


CONTENT_TYPE = 'application/vnd.api+json'


def autodiscover():
    """
    Automatically discovers `resources` modules in `INSTALLED_APPS`.
    """

    discover(api)


def discover(app):
    autodiscover_modules('resources', register_to=app)

    if settings.AUTH_RESOURCES:
        from shanghai.contrib.auth.resources import GroupResource, UserResource

        app.register(GroupResource)
        app.register(UserResource)


def autoinspect():
    """
    Automatically inspects registered resources.
    """

    inspect(api)


def inspect(app):
    app.inspect()


default_app_config = 'shanghai.apps.ShanghaiConfig'


# Register a globally available instance of the Shanghai application.
api = Shanghai()
