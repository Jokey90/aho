from django.db import models
from django.utils.timezone import now
from service.models import Provider, ChecklistValue


def file_path(instance, filename):
    from datetime import date
    return 'photos/service_tickets/{0}/{1}/{2}/{3}'.format(date.today().year, date.today().month, date.today().day, filename)


class Ticket(models.Model):

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    #STATES = [
    #    ('active', 'В работе'),
    #    ('closed', 'Закрыта')
    #]

    #state = models.CharField(verbose_name='Статус', choices=STATES, max_length=10, default='active', blank=False, null=False)
    subject = models.CharField(verbose_name='Тема', max_length=255, blank=False, null=False)
    provider = models.ForeignKey(to=Provider, verbose_name='Провайдер', blank=False, null=False)
    issue = models.ForeignKey(to=ChecklistValue, verbose_name='Замечание', blank=True, null=True)
    text = models.TextField(verbose_name='Содержание', max_length=1000, blank=True, null=True)
    mail_sent = models.BooleanField(verbose_name='Письмо отправлено', default=False, blank=True, null=False)
    creation_datetime = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, blank=True, null=False)
    close_date = models.DateField(verbose_name='Дата закрытия', blank=True, null=True)
    photo = models.FileField(verbose_name='Фото', blank=True, upload_to=file_path, null=True)

    def __str__(self):
        return self.subject
