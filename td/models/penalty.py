from django.db import models
from td.models import Car


class Penalty(models.Model):



    class Meta:
        verbose_name = 'Штраф'
        verbose_name_plural = 'Штрафы'

    car = models.ForeignKey(verbose_name='Автомобиль', blank=False, null=False, to=Car)
    number = models.CharField(verbose_name='Номер постановления', max_length=50, blank=False, null=False)
    date = models.DateField(verbose_name='Дата', blank=False, null=False)
    description = models.CharField(verbose_name='Нарушение', max_length=100, blank=False, null=False)
    amount = models.DecimalField(verbose_name='Сумма', max_digits=10, decimal_places=2, blank=False, null=False, default=0)
    obtain_date = models.DateField(verbose_name='Дата передачи водителю', blank=True, null=True)
    payed = models.BooleanField(verbose_name='Оплачен', default=False, blank=False, null=False)
    pay_date = models.DateField(verbose_name='Дата оплаты', blank=True, null=True)
    driver = models.ForeignKey(verbose_name='Водитель', to='Driver', blank=True, null=True)
    scan = models.FileField(verbose_name='Скан', blank=True, upload_to='scans/penalties/', null=True)
