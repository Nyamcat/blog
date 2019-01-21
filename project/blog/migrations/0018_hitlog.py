# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-01-21 10:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0017_comment_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='HitLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=None, null=True)),
                ('post', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.SummerNote')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
