from django.db import models


class BudgetItem(models.Model):

    class Meta:
        verbose_name = 'Статья бюджета'
        verbose_name_plural = 'Статьи бюджета'

    name = models.CharField(verbose_name='Название статьи', max_length=100, blank=False, null=False, default='')

    def __str__(self):
        return self.name
