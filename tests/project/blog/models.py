from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=256)
    perex = models.CharField(max_length=512)

    category = models.ForeignKey('Category', related_name='articles', null=True, blank=True)

    tags = models.ManyToManyField('Tag', related_name='articles', blank=True)

    def __str__(self):
        return self.title


class ExtendedArticle(models.Model):

    article = models.OneToOneField(Article, related_name="extended_article", null=True, blank=True)

    is_extended = models.BooleanField(default=True, blank=True)


class Category(models.Model):

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class ExtendedTag(models.Model):

    tag = models.OneToOneField(Tag, related_name="extended_tag", primary_key=True)

    is_extended = models.BooleanField(default=True, blank=True)
