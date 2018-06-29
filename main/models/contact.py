from django.db import models


class Contact(models.Model):

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['phone_number']

    name = models.CharField(verbose_name='Название', max_length=100, blank=False, null=False)
    address = models.CharField(verbose_name='Адрес', max_length=255, blank=True, null=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=20, blank=True, null=True)
    person_name = models.CharField(verbose_name='Контактное лицо', max_length=100, blank=True, null=True)
    email = models.EmailField(verbose_name='Электронная почта', blank=True, null=True)
    comment = models.CharField(verbose_name='Комментарий', max_length=1000, blank=True, null=True)
    active = models.BooleanField(verbose_name='Активен', blank=False, null=False, default=True)

    def __str__(self):
        return self.name
