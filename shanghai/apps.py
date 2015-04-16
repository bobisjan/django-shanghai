from django.apps import AppConfig


class Shanghai(object):
    """
    A main class for a Shanghai application.
    """

    name = 'shanghai'
    verbose_name = 'Shanghai'

    def __init__(self):
        self._registry = dict()

    def register(self, resource):
        """
        Registers a resource in the application by it's name.

        :param resource: A resource class to register
        """
        instance = resource(self)
        self._registry[instance.name] = instance

    def resource_for(self, name):
        """
        Lookups for a resource by the provided name.

        :param name: Name of the resource
        :return: Resource or `None` if not found
        """
        return self._registry.get(name, None)

    def inspect(self):
        for resource in self._registry.values():
            resource.inspector.inspect_id()
            resource.inspector.inspect_attributes()
            resource.inspector.inspect_belongs_to()

        for resource in self._registry.values():
            resource.inspector.inspect_has_many()

    def get_urls(self):
        """
        Iterates over the registered resources and ask for their URLs.

        :return: A list of URL patterns from registered resources
        """
        from django.conf.urls import patterns, include

        pattern_list = list()

        for name in sorted(self._registry.keys()):
            resource = self._registry.get(name)
            pattern_list.append(('', include(resource.urls)))

        return patterns('', *pattern_list)

    @property
    def urls(self):
        return self.get_urls()


class ShanghaiConfig(AppConfig):
    """
    A default configuration for a Shanghai application.
    """

    name = Shanghai.name
    verbose_name = Shanghai.verbose_name

    def ready(self):
        super(ShanghaiConfig, self).ready()
        self.module.autodiscover()
        self.module.autoinspect()
