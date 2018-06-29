from django.db import models

from main.structures import MONTHS
from td.models import Car


class MileageManager(models.Manager):
    def with_periods(self):
        from django.db.models import ExpressionWrapper, F, IntegerField
        return super(MileageManager, self).get_queryset().annotate(
            period=ExpressionWrapper(F('year')*100+F('month'), output_field=IntegerField())
        )


class Mileage(models.Model):

    class Meta:
        verbose_name = 'Пробег'
        verbose_name_plural = 'Пробеги'

    year = models.IntegerField(verbose_name='Год', blank=False, null=False)
    month = models.IntegerField(verbose_name='Месяц', choices=MONTHS, blank=False, null=False)
    car = models.ForeignKey(verbose_name='Автомобиль', to=Car, blank=False, null=False)
    value = models.DecimalField(verbose_name='Показания одометра на конец месяца', default=0, blank=False, null=False, decimal_places=2, max_digits=10)
    gasoline = models.DecimalField(verbose_name='Расходы на бензин', default=0, blank=False, null=False, decimal_places=2, max_digits=10)
    objects = MileageManager()

    def prev_mileage(self):
        return Mileage.objects.with_periods().filter(car=self.car, period__lt=self.period).order_by('-year', '-month').first()

    def diff(self):
        if self.prev_mileage():
            return self.value - self.prev_mileage().value
        else:
            return 0

    def gasoline_rate(self):
        if self.diff() > 0 and self.gasoline > 0:
            return self.gasoline / self.diff()
        else:
            return 0
