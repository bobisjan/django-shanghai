from django.core.exceptions import ObjectDoesNotExist


class RelationshipDoesNotExist(ObjectDoesNotExist):

    def __init__(self, resource, relationship):
        self.resource = resource
        self.relationship = relationship

    def __str__(self):
        return 'Relationship `{1}` does not exist on resource `{0}`.'.format(self.resource, self.relationship)
