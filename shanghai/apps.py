from django.apps import AppConfig


class ShanghaiConfig(AppConfig):
    """
    A default configuration for a Shanghai application.
    """

    name = 'shanghai'
    verbose_name = 'Shanghai'

    def ready(self):
        super(ShanghaiConfig, self).ready()
        self.module.autodiscover()
