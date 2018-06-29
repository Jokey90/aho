from django.db import models


class Zone(models.Model):

    class Meta:
        verbose_name = 'Зона'
        verbose_name_plural = 'Зоны'
        ordering = ['block', 'ord_number']

    BLOCKS = [
        [0, 'Клининг'],
        [1, 'Техническая эксплуатация'],
        [2, 'Флористика'],
    ]

    name = models.CharField(verbose_name='Название', max_length=100, blank=False, null=False)
    block = models.IntegerField(verbose_name='Блок', choices=BLOCKS, blank=False, null=False)
    ord_number = models.IntegerField(verbose_name='Порядоковый номер', blank=False, null=False, default=0)

    def __str__(self):
        return self.name
