# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-27 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0003_auto_20170424_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractchange',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='contractchange',
            name='sim',
        ),
        migrations.AddField(
            model_name='bill',
            name='contract',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mobile.Contract', verbose_name='Договор'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sim',
            name='number',
            field=models.CharField(max_length=15, unique=True, verbose_name='Номер'),
        ),
        migrations.DeleteModel(
            name='ContractChange',
        ),
    ]
