class Property(object):
    """
    A base class for resource properties.
    """

    def __init__(self, name=None):
        self.name = name

    def get_from(self, obj):
        return getattr(obj, self.name, None)

    def set_to(self, obj, value):
        setattr(obj, self.name, value)

    def __str__(self):
        return self.name


class Id(Property):
    """
    Represents an identifier of a resource.
    """

    def __init__(self, name='id'):
        super(Id, self).__init__(name)


class Attribute(Property):
    """
    Represents an attribute on a resource.
    """
    pass


class Relationship(Property):
    """
    A base class for resource relationships.
    """

    def __init__(self, target, inverse, kind, name=None):
        super(Relationship, self).__init__(name=name)
        self.target = target
        self.inverse = inverse
        self.kind = kind

    def is_belongs_to(self):
        return self.kind == 'belongs_to'

    def is_has_many(self):
        return self.kind == 'has_many'


class BelongsTo(Relationship):
    """
    Represents a `belongs to` relationship on a resource.
    """

    def __init__(self, target, inverse, name=None):
        super(BelongsTo, self).__init__(target, inverse, kind='belongs_to', name=name)


class HasMany(Relationship):
    """
    Represents a `has many` relationship on a resource.
    """

    def __init__(self, target, inverse, name=None):
        super(HasMany, self).__init__(target, inverse, kind='has_many', name=name)
