from django.db import models
from main.models import Employee


class VisitorsParking(models.Model):

    class Meta:
        verbose_name = 'Гостевой мешиноместо'
        verbose_name_plural = 'Гостевые машиноместа'

    date = models.DateField(verbose_name='Дата', blank=False, null=False)
    time = models.TimeField(verbose_name='Время приезда', blank=True, null=True)
    end_time = models.TimeField(verbose_name='Время выезда', blank=True, null=True)
    car_number = models.CharField(verbose_name='Номер автомобиля', blank=False, null=False, max_length=50)
    visitors_name = models.CharField(verbose_name='Контрагент(гость)', blank=True, null=True, default='', max_length=100)
    invited_by = models.ForeignKey(verbose_name='Инициатор(работник НСД)', to=Employee, blank=False, null=False)
    comment = models.CharField(verbose_name='Комментарий', max_length=100, blank=True, null=True)
