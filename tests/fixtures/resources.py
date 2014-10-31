from shanghai.resources import Resource
from shanghai import meta


class ArticleResource(Resource):

    name = 'articles'

    class Meta:
        title = meta.Attribute()
        perex = meta.Attribute()
        category = meta.BelongsTo('categories', inverse='articles')


class CategoryResource(Resource):

    name = 'categories'

    class Meta:
        id = meta.Id()
        title = meta.Attribute()
        articles = meta.HasMany('articles', inverse='category')
