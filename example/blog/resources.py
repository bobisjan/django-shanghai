from shanghai import api
from shanghai.resources import Resource

from .models import Article, Category


class ArticleResource(Resource):

    name = 'articles'
    model = Article


class CategoryResource(Resource):

    name = 'categories'
    model = Category


api.register(ArticleResource)
api.register(CategoryResource)
