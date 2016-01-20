# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(unique=True, max_length=40)),
                ('first_name', models.CharField(blank=True, max_length=40)),
                ('last_name', models.CharField(blank=True, max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('profile_picture', models.CharField(blank=True, default='https://secure.gravatar.com/avatar/04e0b5943d4bc863c3f46324111fa444.jpg?s=215&r=g&d=identicon', max_length=256)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
