from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=256)
    perex = models.CharField(max_length=512)
    category = models.ForeignKey('Category', related_name='articles', null=True, blank=True)

    def __str__(self):
        return self.title


class Category(models.Model):

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
