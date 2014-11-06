"""
Shanghai settings.
"""

from django import conf


_default_settings = {
    'CONTENT_TYPE': 'application/vnd.api+json',
    'AUTH_RESOURCES': True
}


class Settings(object):

    @staticmethod
    def prefix(name):
        return 'SHANGHAI_' + name

    def __getattr__(self, name):
        if name not in _default_settings:
            raise AttributeError

        return getattr(conf.settings, self.prefix(name), _default_settings[name])


settings = Settings()
