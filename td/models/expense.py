from django.db import models
from td.models import Car, BudgetSubitem


class Expense(models.Model):

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'

    date = models.DateField(verbose_name='Дата', blank=False, null=False)
    car = models.ForeignKey(verbose_name='Автомобиль', to=Car, blank=False, null=False)
    driver = models.ForeignKey(verbose_name='Водитель', to='Driver', blank=False, null=False)
    budget_subitem = models.ForeignKey(verbose_name='Статья расходов', to=BudgetSubitem, blank=False, null=False)
    amount = models.DecimalField(verbose_name='Сумма', blank=False, null=False, default=0, max_digits=12, decimal_places=2)
    active = models.BooleanField(verbose_name='Активна', blank=False, null=False, default=True)
    comment = models.CharField(verbose_name='Комментарий', blank=True, null=False, default='', max_length=100)