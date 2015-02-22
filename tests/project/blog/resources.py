from shanghai import api
from shanghai.resources import ModelResource

from .models import Article, Category, ExtendedArticle, ExtendedTag, Tag


class ArticleResource(ModelResource):

    model = Article


class CategoryResource(ModelResource):

    model = Category


class ExtendedArticleResource(ModelResource):

    model = ExtendedArticle


class ExtendedTagResource(ModelResource):

    model = ExtendedTag


class TagResource(ModelResource):

    model = Tag


api.register(ArticleResource)
api.register(CategoryResource)
api.register(ExtendedArticleResource)
api.register(ExtendedTagResource)
api.register(TagResource)
