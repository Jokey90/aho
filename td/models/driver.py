from django.db import models


class Driver(models.Model):
    from main.models import Employee

    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    emp = models.OneToOneField(verbose_name='Сотрудник', to=Employee, blank=False, null=False)
    comment = models.CharField(verbose_name='Комментарий', blank=True, null=True, default='', max_length=255)
    license = models.CharField(verbose_name='Вод. удостоверение', blank=True, null=True, default='', max_length=100)
    license_date = models.DateField(verbose_name='Вод. удостоверение до', blank=False, null=False)
    phone = models.CharField(verbose_name='Телефон', blank=True, null=True, default='', max_length=100)
    active = models.BooleanField(verbose_name='Активен', blank=False, null=False, default=True)
    photo = models.FileField(verbose_name='Скан вод. удостоверения', blank=True, upload_to='scans/licenses/', null=True)

    def short_name(self):
        return self.emp.short_name()

    def __str__(self):
        return self.emp.short_name()