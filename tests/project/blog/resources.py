from shanghai import api
from shanghai.resources import ModelResource

from .models import Article, Category, ExtendedArticle, ExtendedTag, Tag


class ArticleResource(ModelResource):

    name = 'articles'
    model = Article


class CategoryResource(ModelResource):

    name = 'categories'
    model = Category


class ExtendedArticleResource(ModelResource):

    name = 'extended_articles'
    model = ExtendedArticle


class ExtendedTagResource(ModelResource):

    name = 'extended_tags'
    model = ExtendedTag


class TagResource(ModelResource):

    name = "tags"
    model = Tag


api.register(ArticleResource)
api.register(CategoryResource)
api.register(ExtendedArticleResource)
api.register(ExtendedTagResource)
api.register(TagResource)
