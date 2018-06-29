from django.db import models
from django.utils.timezone import now


class Limit(models.Model):
    from mobile.models import Sim

    class Meta:
        verbose_name = 'Лимит'
        verbose_name_plural = 'Лимиты'

    sim = models.ForeignKey(to=Sim, verbose_name='SIM-карта', blank=False, null=False)
    amount = models.IntegerField('Лимит', default=0, blank=False, null=False)
    infinite = models.BooleanField(verbose_name='Безлимитный', default=False, blank=False, null=False)
    date = models.DateField(verbose_name='Начало периода', blank=False, null=False, default=now)

    def __str__(self):
        return self.sim.number + ' limit ' + str(self.amount) + ' from ' + str(self.date)
