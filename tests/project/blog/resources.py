from shanghai import api
from shanghai.resources import ModelResource

from .models import Article, Category, Tag


class ArticleResource(ModelResource):

    name = 'articles'
    model = Article


class CategoryResource(ModelResource):

    name = 'categories'
    model = Category


class TagResource(ModelResource):

    name = "tags"
    model = Tag


api.register(ArticleResource)
api.register(CategoryResource)
api.register(TagResource)
