# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('namepoll', '0003_suggestion_suggestion_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='selector',
            options={'ordering': ['account']},
        ),
        migrations.RemoveField(
            model_name='selector',
            name='name',
        ),
        migrations.AlterField(
            model_name='suggestion',
            name='suggestion_type',
            field=models.CharField(choices=[('0', 'Yes'), ('1', 'Maybe'), ('2', 'No')], default='0', max_length=1),
        ),
    ]
