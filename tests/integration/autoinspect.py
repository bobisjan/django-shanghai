from tests.test_cases import TestCase

from shanghai.properties import Id, Attribute, BelongsTo, HasMany


class ModelInspectionTesCase(TestCase):

    def test_model_resource_should_have_id(self):
        self._test_for_id('articles')
        self._test_for_id('categories')
        self._test_for_id('extended_articles')
        self._test_for_id('extended_tags')
        self._test_for_id('tags')

    def test_model_resource_should_have_attributes(self):
        self._test_for_attributes('articles', ('title', 'perex'))
        self._test_for_attributes('categories', ('name',))
        self._test_for_attributes('extended_articles', ('is_extended',))
        self._test_for_attributes('extended_tags', ('is_extended',))
        self._test_for_attributes('tags', ('name',))

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

    def _test_for_id(self, resource_name):
        resource = self.api.resource_for(resource_name)

        self.assertIsInstance(resource.get_id(), Id)

    def _test_for_attributes(self, resource_name, attribute_names):
        resource = self.api.resource_for(resource_name)
        attributes = resource.get_attributes()

        for name in attribute_names:
            attr = attributes.get(name, None)

            self.assertIsNotNone(attr)
            self.assertIsInstance(attr, Attribute)

    def _test_for_relationships(self, resource_name, relationships):
        resource = self.api.resource_for(resource_name)
        _relationships = resource.get_relationships()

        for name, rel_class in relationships.items():
            rel = _relationships.get(name, None)

            self.assertIsNotNone(rel)
            self.assertIsInstance(rel, rel_class)
