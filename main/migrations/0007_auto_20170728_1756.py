# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-28 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_globalsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsettings',
            name='name',
            field=models.CharField(default='-', max_length=100, verbose_name='Имя'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='globalsettings',
            name='key',
            field=models.CharField(max_length=100, unique=True, verbose_name='Ключ'),
        ),
    ]