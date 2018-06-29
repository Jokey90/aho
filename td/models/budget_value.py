from django.db import models

from main.structures import MONTHS
from td.models import Car, BudgetSubitem


class BudgetValue(models.Model):

    class Meta:
        verbose_name = 'Знечение бюджета'
        verbose_name_plural = 'Значения бюджета'

    year = models.IntegerField(verbose_name='Год', blank=False, null=False)
    month = models.IntegerField(verbose_name='Месяц', blank=False, null=False, choices=MONTHS)
    car = models.ForeignKey(verbose_name='Автомобиль', to=Car, blank=False, null=False)
    amount = models.DecimalField(verbose_name='Сумма', blank=False, null=False, default=0, decimal_places=2, max_digits=12)
    budget_subitem = models.ForeignKey(verbose_name='Статья расходов', blank=False, null=False, to=BudgetSubitem)
