from django.db import models


class Tariff(models.Model):
    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    name = models.CharField(verbose_name='Название тарифа', max_length=50, blank=False, null=False)
    description = models.CharField(verbose_name='Описание тарифа', max_length=255, blank=True, null=False, default='')
    active = models.BooleanField(verbose_name='Актуальный', default=True, blank=False, null=False)

    def __str__(self):
        return self.name
