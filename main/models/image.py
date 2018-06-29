from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ["name"]

    name = models.CharField(verbose_name='Имя файла', max_length=255, blank=False, null=False)
    file = models.FileField(verbose_name='Файл', blank=False, upload_to='images')
    added_by = models.ForeignKey(User, blank=False)
    add_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return self.name
