from django.db import models
from datetime import datetime


class Transition(models.Model):
    from main.models import Employee
    from mobile.models import Sim

    class Meta:
        verbose_name = 'Передача SIM-карты'
        verbose_name_plural = 'Передачи SIM-карты'

    sim = models.ForeignKey(to=Sim, verbose_name='SIM-карта', blank=False, null=False)
    employee = models.ForeignKey(to=Employee, verbose_name='Сотрудник', blank=False, null=False)
    date = models.DateTimeField(verbose_name='Дата передачи', blank=False, null=False, default=datetime(2000, 1, 1))
    comment = models.CharField(verbose_name='Комментарий', max_length=1000, blank=True, null=False, default='')

    def __str__(self):
        return self.sim.number + ' ' + self.employee.short_name() + ' ' + str(self.date)

    def prev_owner(self):
        prev_transitions = Transition.objects.filter(sim=self.sim, date__lt=self.date).order_by('-date')
        if len(prev_transitions) > 0:
            return prev_transitions.first().employee
        else:
            return None
