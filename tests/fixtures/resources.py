from shanghai.resources import BaseResource
from shanghai import meta


class ArticleResource(BaseResource):

    name = 'articles'

    class Meta:
        title = meta.Attribute()
        perex = meta.Attribute()
        category = meta.BelongsTo('categories', inverse='articles')


class CategoryResource(BaseResource):

    name = 'categories'

    class Meta:
        id = meta.Id()
        title = meta.Attribute()
        articles = meta.HasMany('articles', inverse='category')
