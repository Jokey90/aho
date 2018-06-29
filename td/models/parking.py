from django.db import models
from main.models import Employee


class Parking(models.Model):

    class Meta:
        verbose_name = 'Парковочное место'
        verbose_name_plural = 'Парковочные места'

    PAYMENT_TYPES = (
        (0, '100%'),
        (1, 'Субаренда'),
    )

    BASISES = (
        (0, 'ДДА'),
    )

    number = models.IntegerField(verbose_name='Номер машиноместа', blank=False, null=False)
    car_name = models.CharField(verbose_name='Автомобиль', blank=True, null=True, default='', max_length=50)
    owner = models.ForeignKey(verbose_name='За кем акреплено', to=Employee, blank=True, null=True)
    payment_type = models.IntegerField(verbose_name='Условия оплаты', choices=PAYMENT_TYPES, blank=True, null=True)
    contract = models.CharField(verbose_name='Договор', max_length=100, blank=True, null=True, default='')
    contract_date = models.DateField(verbose_name='Срок договора', blank=True, null=True)
    floor_number = models.IntegerField(verbose_name='Этаж', blank=False, null=False, default=1)
    grade = models.IntegerField(verbose_name='Грейд', blank=True, null=True)
    basis = models.IntegerField(verbose_name='Основание', blank=True, null=True, choices=BASISES)
    comment = models.CharField(verbose_name='Примечение', blank=True, null=False, default='', max_length=1000)
