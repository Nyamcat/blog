# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-20 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20180620_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='summernote',
            name='noc',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
