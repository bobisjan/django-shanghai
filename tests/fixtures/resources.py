from shanghai.resources import Resource
from shanghai.properties import Id, Attribute, BelongsTo, HasMany


class ArticleResource(Resource):

    name = 'articles'

    class Meta:
        title = Attribute()
        perex = Attribute()
        category = BelongsTo('categories', inverse='articles')


class CategoryResource(Resource):

    name = 'categories'

    class Meta:
        id = Id()
        title = Attribute()
        articles = HasMany('articles', inverse='category')
