# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-26 17:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='creation_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='mail_sent',
            field=models.BooleanField(default=False, verbose_name='Письмо отправлено'),
        ),
    ]
