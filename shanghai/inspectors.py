import inspect

from django.db import models

from shanghai.meta import Id, Attribute, BelongsTo, HasMany
from shanghai.utils import resource_for_model


class Inspector(object):

    def __init__(self, resource):
        self.resource = resource

    def inspect_id(self):
        setattr(self.resource, 'id', Id())

    def inspect_attributes(self):
        setattr(self.resource, 'attributes', dict())

    def inspect_belongs_to(self):
        setattr(self.resource, 'relationships', dict())

    def inspect_has_many(self):
        pass


class MetaInspector(Inspector):

    def get_meta(self):
        return getattr(self.resource, 'Meta')

    def inspect_id(self):
        _id = None
        meta = self.get_meta()

        for name, value in inspect.getmembers(meta):
            if issubclass(type(value), Id):
                _id = value

        if not _id:
            _id = Id()

        setattr(self.resource, 'id', _id)

    def inspect_attributes(self):

        attributes = getattr(self.resource, 'attributes', dict())
        meta = self.get_meta()

        for name, value in inspect.getmembers(meta):
            if issubclass(type(value), Attribute):
                if not value.name:
                    value.name = name
                attributes[value.name] = value

        setattr(self.resource, 'attributes', attributes)

    def inspect_belongs_to(self):

        relationships = getattr(self.resource, 'relationships', dict())
        meta = self.get_meta()

        for name, value in inspect.getmembers(meta):
            if issubclass(type(value), BelongsTo):
                if not value.name:
                    value.name = name
                relationships[value.name] = value

        setattr(self.resource, 'relationships', relationships)

    def inspect_has_many(self):

        relationships = getattr(self.resource, 'relationships', dict())
        meta = self.get_meta()

        for name, value in inspect.getmembers(meta):
            if issubclass(type(value), HasMany):
                if not value.name:
                    value.name = name
                relationships[value.name] = value

        setattr(self.resource, 'relationships', relationships)


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

    @staticmethod
    def is_attribute(field_name, field):
        types = models.BigIntegerField, models.BooleanField, models.CharField, models.CommaSeparatedIntegerField, \
                models.DateField, models.DateTimeField, models.DecimalField, models.EmailField, models.FloatField, \
                models.IntegerField, models.GenericIPAddressField, models.NullBooleanField, \
                models.PositiveIntegerField, models.PositiveSmallIntegerField, models.SlugField, \
                models.SmallIntegerField, models.TextField, models.TimeField, models.URLField,

        return issubclass(type(field), types)

    @staticmethod
    def attribute(field_name, field):
        return Attribute(name=field_name)

    @staticmethod
    def is_belongs_to(field_name, field):
        return issubclass(type(field), models.ForeignKey)

    @staticmethod
    def belongs_to(field_name, field):
        resource = resource_for_model(field.rel.to)
        inverse = field.rel.related_name

        return BelongsTo(target=resource.name, inverse=inverse, name=field_name)

    def inspect_id(self):
        _id = None

        for field_name in self.get_all_model_field_names():
            field = self.get_model_field(field_name)

            primary_key = getattr(field, 'primary_key', False)
            if primary_key:
                _id = Id(field_name)
                break
        setattr(self.resource, 'id', _id)

    def inspect_attributes(self):
        attributes = dict()

        for field_name in self.get_all_model_field_names():
            field = self.get_model_field(field_name)

            if self.is_attribute(field_name, field):
                attribute = self.attribute(field_name, field)
                if attribute:
                    attributes[attribute.name] = attribute
        setattr(self.resource, 'attributes', attributes)

    def inspect_belongs_to(self):
        relationships = getattr(self.resource, 'relationships', dict())

        for field_name in self.get_all_model_field_names():
            field = self.get_model_field(field_name)

            if self.is_belongs_to(field_name, field):
                relationship = self.belongs_to(field_name, field)
                if relationship:
                    relationships[relationship.name] = relationship
        setattr(self.resource, 'relationships', relationships)

    def inspect_has_many(self):
        for field_name in self.get_all_model_field_names():
            field = self.get_model_field(field_name)

            if self.is_belongs_to(field_name, field):
                self.add_has_many_from_belongs_to(field_name, field)

    def add_has_many_from_belongs_to(self, field_name, field):
        resource = resource_for_model(field.rel.to)
        relationships = getattr(resource, 'relationships', dict())
        name = field.rel.related_name

        relationship = HasMany(target=self.resource.name, inverse=field_name, name=name)

        relationships[relationship.name] = relationship
        setattr(resource, 'relationships', relationships)
