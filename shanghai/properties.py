from .transforms import transform_for


class Property(object):
    """
    A base class for resource properties.
    """

    def __init__(self, name=None, attr_name=None):
        self.name = name

        if not attr_name and name:
            attr_name = name

        self.attr_name = attr_name

    def get_from(self, obj):
        return getattr(obj, self.attr_name, None)

    def set_to(self, obj, value):
        setattr(obj, self.attr_name, value)

    def __str__(self):
        return self.name


class Id(Property):
    """
    Represents an identifier of a resource.
    """

    def __init__(self, name='id', attr_name=None):
        super(Id, self).__init__(name=name, attr_name=attr_name)


class Attribute(Property):
    """
    Represents an attribute on a resource.
    """

    def __init__(self, kind, transform=None, name=None, attr_name=None):
        super(Attribute, self).__init__(name=name, attr_name=attr_name)

        self.kind = kind
        self.transform = transform or transform_for(self.kind)


class Relationship(Property):
    """
    A base class for resource relationships.
    """

    def __init__(self, target, inverse, kind, name=None, attr_name=None):
        super(Relationship, self).__init__(name=name, attr_name=attr_name)
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

    def __init__(self, target, inverse, name=None, attr_name=None):
        super(BelongsTo, self).__init__(target, inverse, kind='belongs_to', name=name, attr_name=attr_name)


class HasMany(Relationship):
    """
    Represents a `has many` relationship on a resource.
    """

    def __init__(self, target, inverse, name=None, attr_name=None):
        super(HasMany, self).__init__(target, inverse, kind='has_many', name=name, attr_name=attr_name)
