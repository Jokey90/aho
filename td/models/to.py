from django.db import models
from td.models import Car


class TO(models.Model):

    class Meta:
        verbose_name = 'Тех. обслуживание'
        verbose_name_plural = 'Тех. обслуживание'

    name = models.CharField(verbose_name='Вид обслуживания', blank=True, null=False, default='', max_length=250)
    car = models.ForeignKey(verbose_name='Автомобиль', to=Car, blank=False, null=False)
    date = models.DateField(verbose_name='Дата', blank=False, null=False)
    mileage = models.IntegerField(verbose_name='Пробег', default=0, blank=False, null=False)
    # fact = models.BooleanField(verbose_name='Пройдено', default=0, blank=False, null=False)
    budget_amount = models.FloatField(verbose_name='Бюджет на ТО', blank=False, null=False, default=0)
    fact_amount = models.FloatField(verbose_name='Факт. расходы', blank=False, null=False, default=0)
    comment = models.CharField(verbose_name='Комментарий', blank=True, null=True, default='', max_length=1000)
