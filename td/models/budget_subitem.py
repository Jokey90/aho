from django.db import models
from td.models import BudgetItem


class BudgetSubitem(models.Model):

    class Meta:
        verbose_name = 'Статья расходов'
        verbose_name_plural = 'Статьи расходов'

    name = models.CharField(verbose_name='Название статьи', max_length=100, blank=False, null=False, default='')
    parent_item = models.ForeignKey(verbose_name='Родительская статья бюджета', to=BudgetItem, blank=False, null=False, related_name='subitems')

    def __str__(self):
        return self.name