# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_email_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='version',
            field=models.CharField(blank=True, default='V1', max_length=2),
        ),
    ]
