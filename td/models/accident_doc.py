from django.db import models


class AccidentDoc(models.Model):
    from td.models import Accident

    class Meta:
        verbose_name = 'документ ДТП'
        verbose_name_plural = 'документы ДТП'

    name = models.CharField(verbose_name='Описание', blank=True, null=False, default='', max_length=100)
    accident = models.ForeignKey(verbose_name='ДТП', to=Accident, blank=False, null=False)
    scan = models.FileField(verbose_name='Скан', blank=True, upload_to='scans/accidents/', null=True)

    def __str__(self):
        return self.name # + ' ' + self.car.name + ' ' + self.car.number
