from django.db import models
from django.utils.timezone import now
from main.models import Floor


class ChecklistManager(models.Manager):
    def with_issues(self):
        return self.model.objects.extra(where=[
            '(SELECT count(distinct id) FROM service_checklistvalue WHERE checklist_id=service_checklist.id and has_issues=1)>0'])

    def without_issues(self):
        return self.model.objects.extra(where=[
            '(SELECT count(distinct id) FROM service_checklistvalue WHERE checklist_id=service_checklist.id and has_issues=1)=0'])

    def unsolved_only(self):
        return self.model.objects.extra(where=[
            '(SELECT count(distinct id) FROM service_checklistvalue WHERE checklist_id=service_checklist.id and has_issues=1 and solve_date is null)>0'])

    def solved_only(self):
        return self.model.objects.extra(where=[
            '(SELECT count(distinct id) FROM service_checklistvalue WHERE checklist_id=service_checklist.id and has_issues=1 and solve_date is null)=0'])


class Checklist(models.Model):

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'

    STATES = [
        ['new', 'Новый'],
        ['ok', 'Замечаний нет'],
        ['has_issues', 'Есть замечания'],
        ['issues_solved', 'Замечания устранены']
    ]

    date = models.DateField(verbose_name='Дата обхода', default=now, blank=False, null=False)
    floor = models.ForeignKey(verbose_name='Этаж', to=Floor, blank=False, null=False)
    # state = models.CharField(verbose_name='Статус', choices=STATES, max_length=20)
    objects = ChecklistManager()

    def __str__(self):
        return self.date.strftime('%d.%m.%Y') + ' ' + str(self.floor)

    def issues_count(self):
        return self.checklistvalue_set.filter(has_issues=True).count()

    def issues_solved(self):
        return self.checklistvalue_set.filter(has_issues=True, solve_date__isnull=False).count()

    def issues_left(self):
        return self.checklistvalue_set.filter(has_issues=True, solve_date__isnull=True).count()
