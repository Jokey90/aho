from django.db import models


class SimManager(models.Manager):
    def with_month_stats(self, year, month):
        from django.db import connection
        from datetime import date
        import calendar

        date_str = date(year, month, calendar.monthrange(year, month)[1]).strftime('%Y-%m-%d')
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT
                    s.id,
                    s.number,
                    s.active,
                    (SELECT TOP 1 employee_id FROM mobile_transition as t WHERE t.sim_id=s.id and t.date<=%s ORDER BY t.date DESC) as owner_id,
                    coalesce((SELECT TOP 1 l.amount FROM mobile_limit as l WHERE l.sim_id=s.id and l.date<=%s ORDER BY l.date DESC),0) as limit,
                    coalesce((SELECT TOP 1 l.infinite FROM mobile_limit as l WHERE l.sim_id=s.id and l.date<=%s ORDER BY l.date DESC),0) as limit_infinite,
                    (SELECT SUM(b.amount) FROM mobile_bill as b WHERE b.sim_id=s.id and year(b.period)=%s and month(b.period)=%s) as bill_amount
                FROM
                    mobile_sim as s
                ORDER BY
                    s.number''', (date_str, date_str, date_str, year, month))
            result_list = []
            for row in cursor.fetchall():
                sim = self.model(id=row[0], number=row[1], active=row[2])
                sim.owner_id = row[3]
                sim.limit = row[4]
                sim.limit_infinite = row[5]
                sim.bill_amount = row[6]
                result_list.append(sim)
        return result_list

    def with_current_stats(self):
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT
                    t.id,
                    t.number,
                    t.active,
                    t.owner_id,
                    coalesce((SELECT last_name+' '+first_name+' '+middle_name FROM main_employee WHERE id=t.owner_id),'') as owner_name,
                    t.limit,
                    t.limit_infinite,
                    t.tariff_id,
                    t.tariff_name,
                    t.comment
                FROM
                    (SELECT
                        s.id,
                        s.number,
                        s.active,
                        s.tariff_id,
                        coalesce((SELECT name FROM mobile_tariff WHERE id=s.tariff_id),'') as tariff_name,
                        (SELECT TOP 1 employee_id FROM mobile_transition WHERE sim_id=s.id and date<=CURRENT_TIMESTAMP ORDER BY date DESC) as owner_id,
                        coalesce((SELECT TOP 1 l.amount FROM mobile_limit as l WHERE l.sim_id=s.id and l.date<=CURRENT_TIMESTAMP ORDER BY l.date DESC),0) as limit,
                        coalesce((SELECT TOP 1 l.infinite FROM mobile_limit as l WHERE l.sim_id=s.id and l.date<=CURRENT_TIMESTAMP ORDER BY l.date DESC),0) as limit_infinite,
                        s.comment
                    FROM
                        mobile_sim as s) as t
                ORDER BY
                    t.number''')
            result_list = []
            for row in cursor.fetchall():
                sim = self.model(id=row[0], number=row[1], active=row[2])
                sim.owner_id = row[3]
                sim.owner_name = row[4]
                sim.limit = row[5]
                sim.limit_infinite = row[6]
                sim.tariff_id = row[7]
                sim.tariff_name = row[8]
                sim.comment = row[9]
                result_list.append(sim)
        return result_list


class Sim(models.Model):
    from mobile.models import Tariff
    from main.models import Employee

    class Meta:
        verbose_name = 'SIM-карта'
        verbose_name_plural = 'SIM-карты'

    number = models.CharField(verbose_name='Номер', max_length=15, blank=False, null=False, unique=True)
    tariff = models.ForeignKey(to=Tariff, verbose_name='Тариф', blank=True, null=True)
    active = models.BooleanField(verbose_name='Активна', blank=False, null=False, default=True)
    comment = models.CharField(verbose_name='Комментарий', max_length=255, blank=True, null=False, default='')

    objects = SimManager()

    def __str__(self):
        return '('+self.number[0:3]+') '+self.number[3:6]+'-'+self.number[6:8]+'-'+self.number[8:10]

    def current_owner(self):
        from mobile.models import Transition
        from datetime import datetime
        transitions = Transition.objects.filter(sim=self, date__lte=datetime.now()).order_by('-date')
        if len(transitions):
            return transitions.first().employee
        else:
            return None

    def current_limit(self):
        from mobile.models import Limit
        from datetime import date
        limits = Limit.objects.filter(sim=self, date__lte=date.today()).order_by('-date')
        if len(limits):
            if limits.first().infinite:
                return None
            else:
                return limits.first().amount
        else:
            return 0

    current_owner.short_description = 'Текущий владелец'
    current_limit.short_description = 'Текущий лимит'

    def owner_by_date(self, date):
        from mobile.models import Transition
        transitions = Transition.objects.filter(sim=self, date__lte=date).order_by('-date')
        if len(transitions):
            return transitions.first().employee
        else:
            from main.models import Employee
            return Employee.objects.get(id=1804)

    def limit_by_date(self, date):
        from mobile.models import Limit
        limits = Limit.objects.filter(sim=self, date__lte=date).order_by('-date')
        if len(limits):
            if limits.first().infinite:
                return None
            else:
                return limits.first().amount
        else:
            return 0
