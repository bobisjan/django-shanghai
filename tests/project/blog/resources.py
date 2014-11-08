from shanghai import api
from shanghai.resources import ModelResource

from .models import Article, Category, ExtendedArticle, Tag


class ArticleResource(ModelResource):

    name = 'articles'
    model = Article


class CategoryResource(ModelResource):

    name = 'categories'
    model = Category


class ExtendedArticleResource(ModelResource):

    name = 'extended_articles'
    model = ExtendedArticle


class TagResource(ModelResource):

    name = "tags"
    model = Tag


api.register(ArticleResource)
api.register(CategoryResource)
api.register(ExtendedArticleResource)
api.register(TagResource)
