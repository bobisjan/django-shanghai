# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_extendedarticle'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedTag',
            fields=[
                ('tag', models.OneToOneField(serialize=False, related_name='extended_tag', primary_key=True, to='blog.Tag')),
                ('is_extended', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='extendedarticle',
            name='article',
            field=models.OneToOneField(related_name='extended_article', blank=True, null=True, to='blog.Article'),
        ),
    ]
