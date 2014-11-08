from django.contrib import admin

from .models import Article, Category, ExtendedArticle, ExtendedTag, Tag


admin.site.register(Article)
admin.site.register(Category)
admin.site.register(ExtendedArticle)
admin.site.register(ExtendedTag)
admin.site.register(Tag)
