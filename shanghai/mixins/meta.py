from shanghai.exceptions import RelationshipDoesNotExist


class MetaMixin(object):

    def primary_key(self):
        return getattr(self, '_primary_key')

    def attributes(self):
        return getattr(self, '_attributes')

    def attribute_for(self, name):
        attributes = self.attributes()
        return attributes.get(name)

    def relationships(self):
        return getattr(self, '_relationships')

    def relationship_for(self, name):
        relationships = self.relationships()
        relationship = relationships.get(name, None)

        if not relationship:
            raise RelationshipDoesNotExist(self, name)
        return relationship

    def property_for(self, name):
        primary = self.primary_key()
        if primary.name == name:
            return primary

        attributes = self.attributes()
        if name in attributes:
            return attributes.get(name)

        relationships = self.relationships()
        if name in relationships:
            return relationships.get(name)

        return None
