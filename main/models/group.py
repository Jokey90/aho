from django.db import models


class Group(models.Model):

    class Meta:
        verbose_name = 'Группа сотрудников'
        verbose_name_plural = 'Группы сотрудников'
        ordering = ['name']

    name = models.CharField(verbose_name='Название', max_length=100, blank=True, null=True)
    comment = models.CharField(verbose_name='Комментарий', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
