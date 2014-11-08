# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20141104_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('is_extended', models.BooleanField(default=True)),
                ('article', models.OneToOneField(to='blog.Article', related_name='article', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
