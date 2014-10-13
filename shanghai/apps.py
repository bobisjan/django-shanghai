from django.apps import AppConfig


class Shanghai(object):
    """
    A main class for a Shanghai application.
    """

    def __init__(self):
        self._registry = {}


class ShanghaiConfig(AppConfig):
    """
    A default configuration for a Shanghai application.
    """

    name = 'shanghai'
    verbose_name = 'Shanghai'

    def ready(self):
        super(ShanghaiConfig, self).ready()
        self.module.autodiscover()
