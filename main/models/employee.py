from django.db import models
from main.models import Department


class Employee(models.Model):

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['last_name', 'first_name', 'middle_name']

    dv_guid = models.CharField(verbose_name='GUID в DocsVision', max_length=36, blank=True, null=True)
    first_name = models.CharField(verbose_name='Имя', max_length=100, blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=100, blank=False, null=False)
    middle_name = models.CharField(verbose_name='Отчество', max_length=100, blank=True, null=True)
    account_name = models.CharField(verbose_name='Логин', max_length=50, blank=True, null=True)
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    position = models.CharField(verbose_name='Должность', blank=True, null=True, max_length=100)
    department = models.ForeignKey(verbose_name='Подразделение', to=Department, blank=False, null=False)
    active = models.BooleanField(verbose_name='Активен', default=True, blank=False, null=False)
    comment = models.CharField(verbose_name='Комментарий', max_length=255, blank=True, null=True)
    group = models.ForeignKey(to='Group', verbose_name='Группа', blank=True, null=True)

    def short_name(self):
        name = self.last_name
        if self.first_name is not None:
            if len(self.first_name) > 0:
                name += ' ' + self.first_name[0:1] + '.'
        if self.middle_name is not None:
            if len(self.middle_name) > 0:
                name += ' ' + self.middle_name[0:1] + '.'
        return name

    def __str__(self):
        return self.short_name()
