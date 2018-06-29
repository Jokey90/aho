from django.db import models


class ChecklistRow(models.Model):

    class Meta:
        verbose_name = 'Строка отчета'
        verbose_name_plural = 'Строки отчета'
        ordering = ['zone', 'ord_number']

    name = models.CharField(verbose_name='Название', max_length=100, blank=False, null=False)
    zone = models.ForeignKey(verbose_name='Зона', to='Zone')
    ord_number = models.IntegerField(verbose_name='Порядковый номер', blank=False, null=False)

    def __str__(self):
        return self.name
