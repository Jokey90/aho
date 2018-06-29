from django.db import models
from service.models import ChecklistRow, Checklist


def file_path(instance, filename):
    return 'photos/service_issues/{0}/{1}/{2}/{3}'.format(instance.checklist.date.year, instance.checklist.date.month, instance.checklist.date.day, filename)


class ChecklistValue(models.Model):

    class Meta:
        verbose_name = 'Значение строки отчета'
        verbose_name_plural = 'Значения строк отчета'

    checklist = models.ForeignKey(verbose_name='Отчет', to=Checklist, blank=False, null=False)
    row = models.ForeignKey(verbose_name='Строка отчета', to=ChecklistRow, blank=False, null=False)
    has_issues = models.BooleanField(verbose_name='Есть замечания', default=False, blank=False, null=False)
    # issues_solved = models.BooleanField(verbose_name='Замечания устранены', default=False, blank=False, null=False)
    solve_date = models.DateField(verbose_name='Дата устранения', blank=True, null=True)
    photo = models.FileField(verbose_name='Фото', blank=True, upload_to=file_path, null=True)
    comment = models.CharField(verbose_name='Примечания', max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.checklist.date.strftime('%d.%m.%Y') +' ' + self.checklist.floor.name + ': ' + self.row.zone.name + ' - ' + self.row.name

    def has_ticket(self):
        from service.models import Ticket
        return Ticket.objects.filter(issue_id=self.id).exists()

    def get_ticket(self):
        from service.models import Ticket
        return next(iter(Ticket.objects.filter(issue_id=self.id)), None)
