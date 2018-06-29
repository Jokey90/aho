from django.db import models
from main.models import Contact


class Provider(models.Model):

    class Meta:
        verbose_name = 'Сервисный провайдер'
        verbose_name_plural = 'Сервисные провайдеры'

    contact = models.ForeignKey(verbose_name='Контакт', to=Contact)
    name = models.CharField(verbose_name='Название сервиса', max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name
