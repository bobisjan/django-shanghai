from shanghai.exceptions import RelationshipDoesNotExist


class MetaMixin(object):

    def get_id(self):
        return getattr(self, '_id')

    def get_attributes(self):
        return getattr(self, '_attributes')

    def attribute_for(self, name):
        attributes = self.get_attributes()
        return attributes.get(name)

    def get_relationships(self):
        return getattr(self, '_relationships')

    def relationship_for(self, name):
        relationships = self.get_relationships()
        relationship = relationships.get(name, None)

        if not relationship:
            raise RelationshipDoesNotExist(self, name)
        return relationship

    def property_for(self, name):
        primary = self.get_id()
        if primary.name == name:
            return primary

        attributes = self.get_attributes()
        if name in attributes:
            return attributes.get(name)

        relationships = self.get_relationships()
        if name in relationships:
            return relationships.get(name)

        return None
