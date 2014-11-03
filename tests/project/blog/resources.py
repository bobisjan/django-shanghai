from shanghai import api
from shanghai.resources import ModelResource

from .models import Article, Category


class ArticleResource(ModelResource):

    name = 'articles'
    model = Article


class CategoryResource(ModelResource):

    name = 'categories'
    model = Category


api.register(ArticleResource)
api.register(CategoryResource)
