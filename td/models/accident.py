from django.db import models


class Accident(models.Model):
    from td.models import Car, Driver

    class Meta:
        verbose_name = 'ДТП'
        verbose_name_plural = 'ДТП'

    name = models.CharField(verbose_name='Описание', blank=True, null=False, default='', max_length=100)
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    car = models.ForeignKey(verbose_name='Автомобиль', to=Car, blank=False, null=False)
    culprit = models.ForeignKey(verbose_name='Виновник', to=Driver, blank=True, null=True)
    comment = models.CharField(verbose_name='Комментарий', blank=True, null=True, default='', max_length=255)
    # scan = models.FileField(verbose_name='Скан', blank=True, upload_to='scans/accidents/', null=True)

    def __str__(self):
        return self.name # + ' ' + self.car.name + ' ' + self.car.number
