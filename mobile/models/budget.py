from django.db import models


class Budget(models.Model):
    from datetime import datetime
    from main.models import Department

    class Meta:
        verbose_name = 'Бюджет'
        verbose_name_plural = 'Бюджеты'

    year = models.IntegerField(verbose_name='Год', blank=False, null=False, default=datetime.now().year)
    division = models.CharField(verbose_name='Подразделение', blank=False, null=False, choices=Department.DIVISIONS,
                                default='GORN', max_length=10)
    amount = models.FloatField(verbose_name='Сумма', blank=False, null=False, default=0)

    def __str__(self):
        return 'Бюджет ' + self.get_division_display() + ' ' + str(self.year) + ': ' + str(self.amount)
