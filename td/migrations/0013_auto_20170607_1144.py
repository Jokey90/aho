# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-07 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('td', '0012_auto_20170607_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='to',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='to',
            name='name',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='Вид обслуживания'),
        ),
    ]
