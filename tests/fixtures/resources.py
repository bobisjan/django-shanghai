from shanghai.resources import Resource
from shanghai.properties import PrimaryKey, Attribute, BelongsTo, HasMany


class ArticleResource(Resource):

    class Meta:
        title = Attribute('string')
        perex = Attribute('string')
        category = BelongsTo('categories', inverse='articles')


class CategoryResource(Resource):

    class Meta:
        id = PrimaryKey()
        title = Attribute('string')
        articles = HasMany('articles', inverse='category')
