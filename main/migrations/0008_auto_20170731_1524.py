# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-31 15:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20170728_1756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='globalsettings',
            options={'verbose_name': 'Глобальные настройки', 'verbose_name_plural': 'Глобальные настройки'},
        ),
    ]