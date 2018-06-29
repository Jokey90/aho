# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-02 15:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0005_auto_20170502_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='', verbose_name='Файл')),
                ('month', models.IntegerField(choices=[(1, 'январь'), (2, 'февраль'), (3, 'март'), (4, 'апрель'), (5, 'май'), (6, 'июнь'), (7, 'июль'), (8, 'август'), (9, 'сентябрь'), (10, 'октябрь'), (11, 'ноябрь'), (12, 'декабрь')], default=5, verbose_name='Месяц')),
                ('year', models.IntegerField(default=2017, verbose_name='Год')),
            ],
            options={
                'verbose_name_plural': 'Счета',
                'verbose_name': 'Счет',
            },
        ),
        migrations.AlterModelOptions(
            name='bill',
            options={'verbose_name': 'Расход', 'verbose_name_plural': 'Расходы'},
        ),
        migrations.AddField(
            model_name='bill',
            name='bill_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mobile.BillFile', verbose_name='Файл счета'),
        ),
    ]
