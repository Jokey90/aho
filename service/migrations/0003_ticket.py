# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-26 11:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_remove_checklist_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('active', 'В работе'), ('closed', 'Закрыта')], default='active', max_length=10, verbose_name='Статус')),
                ('subject', models.CharField(max_length=255, verbose_name='Тема')),
                ('text', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Содержание')),
                ('issue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service.ChecklistValue', verbose_name='Замечание')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service.Provider', verbose_name='Провайдер')),
            ],
            options={
                'verbose_name_plural': 'Заявки',
                'verbose_name': 'Заявка',
            },
        ),
    ]
