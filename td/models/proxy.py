from django.db import models
from td.models import Car


class Proxy(models.Model):

    class Meta:
        verbose_name = 'Доверенность на вождение'
        verbose_name_plural = 'Доверенности на вождение'

    PROXY_TYPES = (
        (0, 'Доверенность на управление'),
        (1, 'Доверенность на сервис'),
        (2, 'Доверенность на взаимодействие со страховой'),
    )

    car = models.ForeignKey(verbose_name='Автомобиль', to=Car, blank=False, null=False)
    driver = models.ForeignKey(verbose_name='Водитель', to='Driver', blank=False, null=False)
    start_date = models.DateField(verbose_name='Дата начала', blank=False, null=False)
    end_date = models.DateField(verbose_name='Дата окончания', blank=False, null=False)
    type = models.IntegerField(verbose_name='Тип доверенности', blank=False, null=False, default=0, choices=PROXY_TYPES)
    scan = models.FileField(verbose_name='Скан', blank=True, upload_to='scans/proxies/', null=True)
    active = models.BooleanField(verbose_name='Активна', blank=False, null=False, default=True)

    def __str__(self):
        return self.get_type_display() + ' ' + self.car.name + ' ' + self.driver.short_name()

    def current_owner(self):
        from td.models import ProxyTracking
        from datetime import date
        last_moves = ProxyTracking.objects.filter(proxy=self, date__lte=date.today()).order_by('-date', '-id')
        if len(last_moves) > 0:
            return last_moves.first().owner
        else:
            return None

    def last_move_date(self):
        from td.models import ProxyTracking
        from datetime import date
        last_moves = ProxyTracking.objects.filter(proxy=self, date__lte=date.today()).order_by('-date', '-id')
        if len(last_moves) > 0:
            return last_moves.first().date
        else:
            return None

    def former_owner(self, date):
        from td.models import ProxyTracking
        last_moves = ProxyTracking.objects.filter(proxy=self, date__lte=date).order_by('-date', '-id')
        if len(last_moves) > 0:
            return last_moves.first().owner
        else:
            return None
