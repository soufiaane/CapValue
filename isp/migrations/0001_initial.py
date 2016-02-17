# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-07 17:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ISP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isp_name', models.CharField(blank=True, max_length=40)),
                ('logo', models.CharField(blank=True, max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('members', models.ManyToManyField(related_name='isp', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
