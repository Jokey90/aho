from django.db import models


class Contract(models.Model):

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    name = models.CharField(verbose_name='Договор', max_length=50, blank=False, null=False)
    number = models.CharField(verbose_name='Номер довогора', max_length=20, blank=False, null=False)
    group = models.CharField(verbose_name='Группа счетов', max_length=5, blank=False, null=False)
    comment = models.CharField(verbose_name='Комментарий', max_length=255, blank=True, null=False, default='')
    active = models.BooleanField(verbose_name='Активен', default=True, blank=False, null=False)
    mts = models.BooleanField(verbose_name='МТС', default=False, blank=False, null=False)

    def __str__(self):
        return self.name
