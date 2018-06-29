from django.db import models


class Department(models.Model):

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        ordering = ["name"]

    DIVISIONS = [
        ('GORN', 'ГОРН Девелопмент'),
        ('ZEL', 'Аппарат Зеленова')
    ]

    name = models.CharField(verbose_name='Название', max_length=100, blank=False, null=False)
    short_name = models.CharField(verbose_name='Короткое название', max_length=100, blank=True, null=True)
    manager = models.ForeignKey(verbose_name='Руководитель', to='Employee', blank=True, null=True, related_name='controlled_department')
    dv_guid = models.CharField(verbose_name='GUID в DocsVision', max_length=36, blank=True, null=True)
    description = models.CharField(verbose_name='Описание/комментарии', max_length=1000, blank=True, null=True)
    parent_department = models.ForeignKey(verbose_name='Родительское подразделение', to='self', blank=True, null=True)
    # dv_parent_guid = models.CharField(verbose_name='Родительский GUID в DocsVision', max_length=36, blank=True, null=True)
    active = models.BooleanField(verbose_name='Активно', blank=False, null=False, default=True)
    division = models.CharField(verbose_name='Подразделение', blank=True, null=True, choices=DIVISIONS, default='GORN', max_length=10)

    def __str__(self):
        return self.name
