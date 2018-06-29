'''from django.db import models


class ContractChange(models.Model):
    from mobile.models import Sim, Contract

    class Meta:
        verbose_name = 'Изменение договора'
        verbose_name_plural = 'Изменения договоров'

    sim = models.ForeignKey(to=Sim, verbose_name='SIM-карта', blank=False, null=False)
    contract = models.ForeignKey(to=Contract, verbose_name='Договор', blank=False, null=False)
    date = models.DateField(verbose_name='Дата смены договора', blank=False, null=False)
    comment = models.CharField(verbose_name='Комментарий', max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.sim.number + ' ' + str(self.date) + ' ' + self.contract.name
'''