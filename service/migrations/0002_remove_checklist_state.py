# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-18 13:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklist',
            name='state',
        ),
    ]
