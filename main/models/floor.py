from django.db import models


class Floor(models.Model):

    class Meta:
        verbose_name = 'Этаж'
        verbose_name_plural = 'Этажи'
        ordering = ['name']

    name = models.CharField(verbose_name='Название', max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name
