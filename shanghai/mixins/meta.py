from shanghai.exceptions import RelationshipDoesNotExist


class MetaMixin(object):

    def get_id(self):
        return getattr(self, 'id')

    def get_attributes(self):
        return getattr(self, 'attributes')

    def attribute_for(self, name):
        attributes = self.get_attributes()

        return attributes.get(name)

    def get_relationships(self):
        return getattr(self, 'relationships')

    def relationship_for(self, name):
        relationships = self.get_relationships()

        relationship = relationships.get(name, None)

        if not relationship:
            raise RelationshipDoesNotExist(self.name, name)

        return relationship
