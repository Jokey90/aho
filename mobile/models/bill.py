from django.db import models


class BillManager(models.Manager):
    def with_sim_details(self, year, month):
        from django.db import connection
        from datetime import date

        year = int(year)
        month = int(month)

        date_str = date(year, month, 1).strftime('%Y-%m-%d')
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT
                    b.id,
                    b.period,
                    b.amount,
                    coalesce((SELECT TOP 1 number FROM mobile_sim WHERE id=b.sim_id),b.number) as number,
                    b.contract_id,
                    b.bill_file_id,
                    b.sim_id,
                    coalesce((SELECT TOP 1 employee_id FROM mobile_transition as t WHERE t.sim_id=b.sim_id and t.date<=b.period ORDER BY t.date DESC),1804) as owner_id,
                    coalesce((SELECT TOP 1 l.amount FROM mobile_limit as l WHERE l.sim_id=b.sim_id and l.date<=b.period ORDER BY l.date DESC),0) as limit,
                    coalesce((SELECT TOP 1 l.infinite FROM mobile_limit as l WHERE l.sim_id=b.sim_id and l.date<=b.period ORDER BY l.date DESC),0) as limit_infinite,
                    (SELECT TOP 1 name FROM mobile_contract WHERE id=b.contract_id) as contract_name
                FROM
                    mobile_bill as b
                WHERE
                     year(b.period)=%s and month(b.period)=%s
                     and amount>0''', (year, month))
            result_list = []
            for row in cursor.fetchall():
                bill = self.model(id=row[0], period=row[1], amount=row[2], number=row[3], contract_id=row[4], bill_file_id=row[5])
                bill.sim_id = row[6]
                bill.sim_owner_id = row[7]
                bill.sim_limit = row[8]
                bill.sim_limit_infinite = row[9]
                bill.contract_name = row[10]
                result_list.append(bill)
        return result_list


class Bill(models.Model):
    from mobile.models import Sim, Contract

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'
        ordering = ['number', 'sim']

    sim = models.ForeignKey(to=Sim, verbose_name='SIM-карта', blank=True, null=True, on_delete=models.SET_NULL)
    number = models.CharField(verbose_name='Номер', blank=True, null=True, max_length=20)
    period = models.DateField(verbose_name='Период', blank=False, null=False)
    amount = models.FloatField(verbose_name='Сумма', blank=False, null=False, default=0)
    contract = models.ForeignKey(to=Contract, verbose_name='Договор', blank=False, null=False)
    bill_file = models.ForeignKey(to='BillFile', verbose_name='Файл счета', blank=True, null=True)

    objects = BillManager()

    def __str__(self):
        return str(self.number) + ' ' + str(self.period) + ': ' + str(self.amount)

    def owner(self):
        from mobile.models import Transition
        transitions = Transition.objects.filter(sim=self.sim, date__lte=self.period).order_by('-date')
        if len(transitions) > 0:
            return transitions.first().employee
        else:
            return None

    def limit(self):
        from mobile.models import Limit
        limits = Limit.objects.filter(sim=self.sim, date__lte=self.period).order_by('-date')
        if len(limits) > 0:
            if limits.first().infinite:
                return None
            else:
                return limits.first().amount
        else:
            return 0

    def overflow(self):
        if self.limit() is None:
            return 0
        else:
            return self.limit() - self.amount
