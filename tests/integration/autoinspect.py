from tests.test_cases import TestCase

from shanghai.properties import PrimaryKey, Attribute, BelongsTo, HasMany


class ModelInspectionTesCase(TestCase):

    def test_model_resource_should_have_primary_key(self):
        self._test_for_primary_key('articles')
        self._test_for_primary_key('categories')
        self._test_for_primary_key('extended_articles')
        self._test_for_primary_key('extended_tags')
        self._test_for_primary_key('tags')

    def test_model_resource_should_have_attributes(self):
        self._test_for_attributes('articles', (
            {'name': 'title', 'kind': 'string'},
            {'name': 'perex', 'kind': 'string'}
        ))
        self._test_for_attributes('categories', ({'name': 'name', 'kind': 'string'},))
        self._test_for_attributes('extended_articles', ({'name': 'is_extended', 'kind': 'boolean'},))
        self._test_for_attributes('extended_tags', ({'name': 'is_extended', 'kind': 'boolean'},))
        self._test_for_attributes('tags', ({'name': 'name', 'kind': 'string'},))

    def test_model_resource_should_have_relationships(self):
        self._test_for_relationships('articles', {
            'category': BelongsTo,
            'extended_article': BelongsTo,
            'tags': HasMany
        })
        self._test_for_relationships('categories', {'articles': HasMany})
        self._test_for_relationships('extended_articles', {'article': BelongsTo})
        self._test_for_relationships('extended_tags', {'tag': BelongsTo})
        self._test_for_relationships('tags', {
            'articles': HasMany,
            'extended_tag': BelongsTo
        })

    def _test_for_primary_key(self, resource_name):
        resource = self.api.resource_for(resource_name)

        self.assertIsInstance(resource.primary_key(), PrimaryKey)

    def _test_for_attributes(self, resource_name, attribute_dict):
        resource = self.api.resource_for(resource_name)
        attributes = resource.attributes()

        for attr_dict in attribute_dict:
            attr = attributes.get(attr_dict['name'], None)

            self.assertIsNotNone(attr)
            self.assertIsInstance(attr, Attribute)

            self.assertEqual(attr.kind, attr_dict['kind'])

    def _test_for_relationships(self, resource_name, relationships):
        resource = self.api.resource_for(resource_name)
        _relationships = resource.get_relationships()

        for name, rel_class in relationships.items():
            rel = _relationships.get(name, None)

            self.assertIsNotNone(rel)
            self.assertIsInstance(rel, rel_class)
