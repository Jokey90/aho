from django.db import models


class GlobalSettingsManager(models.Manager):
    def get_setting(self, key):
        try:
            setting = self.model.objects.get(key=key)
        except:
            setting = None
        return setting


class GlobalSettings(models.Model):

    class Meta:
        verbose_name = 'Глобальные настройки'
        verbose_name_plural = 'Глобальные настройки'

    key = models.CharField(verbose_name='Ключ', max_length=100, blank=False, null=False, unique=True)
    name = models.CharField(verbose_name='Имя', max_length=100, blank=False, null=False)
    value = models.CharField(verbose_name='Значение', max_length=1000, blank=True, null=True)

    objects = GlobalSettingsManager()
