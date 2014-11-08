import inspect

from django.db import models

from shanghai.properties import Id, Attribute, BelongsTo, HasMany
from shanghai.utils import resource_for_model


class Inspector(object):

    def __init__(self, resource):
        self.resource = resource

        setattr(self.resource, 'id', Id())
        setattr(self.resource, 'attributes', dict())
        setattr(self.resource, 'relationships', dict())

    def inspect_id(self):
        pass

    def inspect_attributes(self):
        pass

    def inspect_belongs_to(self):
        pass

    def inspect_has_many(self):
        pass


class MetaInspector(Inspector):

    def get_meta(self):
        return getattr(self.resource, 'Meta')

    def inspect_id(self):
        _id = None
        meta = self.get_meta()

        for name, value in inspect.getmembers(meta):
            if isinstance(value, Id):
                _id = value

        if not _id:
            _id = Id()

        setattr(self.resource, 'id', _id)

    def inspect_attributes(self):
        attributes = getattr(self.resource, 'attributes')
        meta = self.get_meta()

        for name, value in inspect.getmembers(meta):
            if isinstance(value, Attribute):
                if not value.name:
                    value.name = name
                if not value.attr_name:
                    value.attr_name = name
                attributes[value.name] = value

    def inspect_belongs_to(self):
        relationships = getattr(self.resource, 'relationships')
        meta = self.get_meta()

        for name, value in inspect.getmembers(meta):
            if isinstance(value, BelongsTo):
                if not value.name:
                    value.name = name
                if not value.attr_name:
                    value.attr_name = name
                relationships[value.name] = value

    def inspect_has_many(self):
        relationships = getattr(self.resource, 'relationships')
        meta = self.get_meta()

        for name, value in inspect.getmembers(meta):
            if isinstance(value, HasMany):
                if not value.name:
                    value.name = name
                if not value.attr_name:
                    value.attr_name = name
                relationships[value.name] = value


class ModelInspector(Inspector):

    def get_meta(self):
        model = getattr(self.resource, 'model')

        return getattr(model, '_meta')

    def get_all_model_field_names(self):
        meta = self.get_meta()

        return meta.get_all_field_names()

    def get_model_field(self, field_name):
        meta = self.get_meta()
        fields = getattr(meta, 'fields', dict())

        for field in fields:
            if field.name is field_name:
                return field

        many_to_many = getattr(meta, 'many_to_many', dict())

        for field in many_to_many:
            if field_name == field.name:
                return field

    @staticmethod
    def is_attribute_field(field_name, field):
        types = models.BigIntegerField, models.BooleanField, models.CharField, models.CommaSeparatedIntegerField, \
                models.DateField, models.DateTimeField, models.DecimalField, models.EmailField, models.FloatField, \
                models.IntegerField, models.GenericIPAddressField, models.NullBooleanField, \
                models.PositiveIntegerField, models.PositiveSmallIntegerField, models.SlugField, \
                models.SmallIntegerField, models.TextField, models.TimeField, models.URLField,

        return isinstance(field, types)

    @staticmethod
    def attribute(field_name, field):
        return Attribute(name=field_name)

    @staticmethod
    def is_foreign_key_field(field_name, field):
        return isinstance(field, models.ForeignKey)

    @staticmethod
    def is_one_to_one_field(field_name, field):
        return isinstance(field, models.OneToOneField)

    @staticmethod
    def is_many_to_many_field(field_name, field):
        return isinstance(field, models.ManyToManyField)

    @staticmethod
    def belongs_to(field_name, field):
        resource = resource_for_model(field.rel.to)

        if resource:
            inverse = field.rel.related_name

            return BelongsTo(target=resource.name, inverse=inverse, name=field_name)

    def inspect_id(self):
        _id = None

        for field_name in self.get_all_model_field_names():
            field = self.get_model_field(field_name)
            attr_name = None

            primary_key = getattr(field, 'primary_key', False)

            if primary_key and self.is_one_to_one_field(field_name, field):
                attr_name = field_name + '_id'

            if primary_key:
                _id = Id(attr_name=attr_name)
                break

        setattr(self.resource, 'id', _id)

    def inspect_attributes(self):
        attributes = getattr(self.resource, 'attributes')

        for field_name in self.get_all_model_field_names():
            field = self.get_model_field(field_name)

            if self.is_attribute_field(field_name, field):
                attribute = self.attribute(field_name, field)
                if attribute:
                    attributes[attribute.name] = attribute

    def inspect_belongs_to(self):
        relationships = getattr(self.resource, 'relationships')

        for field_name in self.get_all_model_field_names():
            field = self.get_model_field(field_name)

            if self.is_one_to_one_field(field_name, field):
                self.add_belongs_to_from_one_to_one_field(field_name, field)

            elif self.is_foreign_key_field(field_name, field):
                relationship = self.belongs_to(field_name, field)

                if relationship:
                    relationships[relationship.name] = relationship

    def inspect_has_many(self):
        for field_name in self.get_all_model_field_names():
            field = self.get_model_field(field_name)

            if self.is_one_to_one_field(field_name, field):
                continue

            if self.is_foreign_key_field(field_name, field):
                self.add_has_many_from_belongs_to(field_name, field)
            elif self.is_many_to_many_field(field_name, field):
                self.add_has_many_from_many_to_many(field_name, field)

    def add_belongs_to_from_one_to_one_field(self, field_name, field):
        resource = resource_for_model(field.rel.to)

        if resource:
            relationships = getattr(self.resource, 'relationships')
            inverse = field.rel.related_name

            relationship = BelongsTo(target=resource.name, inverse=inverse, name=field_name)
            relationships[relationship.name] = relationship

            inverse_relationships = getattr(resource, 'relationships')

            inverse_relationship = BelongsTo(target=self.resource.name, inverse=field_name, name=inverse)
            inverse_relationships[inverse_relationship.name] = inverse_relationship

    def add_has_many_from_belongs_to(self, field_name, field):
        resource = resource_for_model(field.rel.to)
        relationships = getattr(resource, 'relationships')
        name = field.rel.related_name

        relationship = HasMany(target=self.resource.name, inverse=field_name, name=name)

        relationships[relationship.name] = relationship

    def add_has_many_from_many_to_many(self, field_name, field):
        # skip when a resource for `through` model is registered
        if resource_for_model(field.rel.through):
            return

        resource = resource_for_model(field.rel.to)

        if not resource:
            return

        relationships = getattr(self.resource, 'relationships')
        relationship = HasMany(target=resource.name, inverse=field.rel.related_name, name=field_name)
        relationships[relationship.name] = relationship

        # add `has_many` on the inverse resource

        inverse_relationships = getattr(resource, 'relationships')
        inverse_relationship = HasMany(target=self.resource.name, inverse=field_name, name=field.rel.related_name)
        inverse_relationships[inverse_relationship.name] = inverse_relationship
