from django.db import models
from datetime import date


def file_path(instance, filename):
    return 'uploads/mobile_bills/{0}/{1}/{2}'.format(instance.year, instance.month, filename)


class BillFile(models.Model):
    from main.structures import MONTHS as months

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    file = models.FileField(verbose_name='Файл', blank=True, null=True, upload_to=file_path)
    month = models.IntegerField(verbose_name='Месяц', choices=months, default=date.today().month,
                                blank=False, null=False)
    year = models.IntegerField(verbose_name='Год', blank=False, null=False, default=date.today().year)
    name = models.CharField(verbose_name='Название', blank=False, null=False, default='', max_length=100)

    def __str__(self):
        return self.name + ' ' + self.months[self.month-1][1] + ' ' + str(self.year)

    def filename(self):
        if self.file:
            return self.file.name.split('/')[-1]
        else:
            return None

    def amount(self):
        from mobile.models import Bill
        from django.db.models import Sum
        return Bill.objects.filter(bill_file=self).aggregate(Sum('amount'))['amount__sum']

    def unlinked_rows(self):
        return self.bill_set.filter(sim=None).count()
