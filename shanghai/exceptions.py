from django.core.exceptions import ObjectDoesNotExist


class ObjectsDoesNotExist(ObjectDoesNotExist):
    pass


class RelationshipDoesNotExist(ObjectDoesNotExist):

    def __init__(self, resource, relationship):
        self.resource = resource
        self.relationship = relationship

    def __str__(self):
        return 'Relationship `{1}` does not exist on resource `{0}`.'.format(self.resource, self.relationship)


class LinkedResourceAlreadyExists(Exception):

    def __init__(self, resource, obj, relationship, link):
        self.resource = resource
        self.object = obj
        self.relationship = relationship
        self.link = link

    def __str__(self):
        return 'Relationship `{2}` on resource `{1}` of `{0}` already has been set with `{3}`.'.format(
            self.resource, self.object, self.relationship, self.link)
