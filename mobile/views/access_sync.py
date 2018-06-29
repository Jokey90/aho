from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.middleware.csrf import rotate_token

conn_str = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=\\\\cds.ru\\fs\\Workgroups2\\Управление ' \
               'по работе с персоналом ДСД\\00.Планирование и отчетность\\_Ключи, Мебель, Моб.связь,\\АХО_be.accdb;'


def access_sync_prepare(request):
    import pyodbc

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute('SELECT count(*) as cnt FROM Сотрудники as s WHERE EXISTS (SELECT * FROM Движение_симок WHERE Владелец=s.ID) and (s.aho_db_id=0 or s.aho_db_id is NULL)')
    if cursor.fetchone().cnt > 0:
        cursor.execute('SELECT ID, ФИО as full_name FROM Сотрудники as s WHERE EXISTS (SELECT * FROM Движение_симок WHERE Владелец=s.ID) and (s.aho_db_id=0 or s.aho_db_id is NULL)')
        emps = []
        for row in cursor.fetchall():
            emps.append(str(row.ID)+' - '+row.full_name)
        context = {
            'message': 'Есть несоответствие в сотрудниках, синхронизация невозможна',
            'list': emps
        }
        return render(request, 'mobile/access_sync_prepare.html', context)

    cursor.execute('SELECT count(*) as cnt FROM (SELECT Номер, count(*) as cnt FROM Симки GROUP BY Номер) as t WHERE cnt>1')
    if cursor.fetchone().cnt > 0:
        context = {'message': 'Есть дублирующиеся номера SIM-карт, синхронизация невозможна'}
        return render(request, 'mobile/access_sync_prepare.html', context)

    cursor.execute('SELECT count(*) as cnt FROM (SELECT Номер, Дата, count(*) as cnt FROM Движение_симок as d GROUP BY Номер, Дата) as t WHERE t.cnt>1')
    if cursor.fetchone().cnt > 0:
        context = {'message': 'Есть повторяющиеся передачи SIM-карт в один день, синхронизация невозможна'}
        return render(request, 'mobile/access_sync_prepare.html', context)

    cursor.execute(
        'SELECT count(*) as cnt FROM (SELECT Номер, Начало_периода, count(*) as cnt FROM Лимиты as d GROUP BY Номер, Начало_периода) as t WHERE t.cnt>1')
    if cursor.fetchone().cnt > 0:
        context = {'message': 'Есть повторяющиеся лимиты на одну SIM-карту в один день, синхронизация невозможна'}
        return render(request, 'mobile/access_sync_prepare.html', context)

    context = {
        'message': 'Все в порядке, синхронизация возможна',
        'ok': True
    }
    return render(request, 'mobile/access_sync_prepare.html', context)


def access_sync(request):
    import pyodbc
    from mobile.models import Sim, Bill, BillFile, Limit, Transition, Contract, Tariff

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute('SELECT ID, Название as nam FROM Тарифы')
    Tariff.objects.all().delete()
    for row in cursor.fetchall():
        tariff = Tariff(name=row.nam, id=row.ID)
        tariff.save()

    cursor.execute('SELECT ID, Номер as num, Тариф as tariff FROM Симки')
    Sim.objects.all().delete()
    for row in cursor.fetchall():
        if row.num != '':
            sim = Sim(number=row.num, id=row.ID, tariff_id=row.tariff)
            sim.save()

    cursor.execute('SELECT d.Номер as num, d.Дата as dat, d.Комментарии as comm, e.aho_db_id FROM Движение_симок as d INNER JOIN Сотрудники as e ON e.ID=d.Владелец')
    Transition.objects.all().delete()
    for row in cursor.fetchall():
        transition = Transition(sim_id=row.num, date=row.dat, employee_id=row.aho_db_id)
        if row.comm is not None:
            transition.comment = row.comm
        transition.save()

    cursor.execute('SELECT Номер as num, Начало_периода as dat, Сумма as amount FROM Лимиты')
    Limit.objects.all().delete()
    for row in cursor.fetchall():
        limit = Limit(sim_id=row.num, date=row.dat, amount=row.amount)
        if row.amount == 0:
            limit.infinite = True
        limit.save()

    cursor.execute('SELECT Номер as num, Период as per, Сумма as amount, Группа as grp FROM Мобсвязь ORDER BY year(Период), month(Период), Группа')
    BillFile.objects.all().delete()
    Bill.objects.all().delete()
    month = None
    year = None
    group = None
    bf = None

    contracts = [c.name for c in Contract.objects.order_by('id').all()]

    for row in cursor.fetchall():
        if month != row.per.month or year != row.per.year or group != row.grp:
            year = row.per.year
            month = row.per.month
            group = row.grp
            bf = BillFile(year=year, month=month)
            bf.name = contracts[group-1] + ' ' + str(year) + ' ' + str(month)
            bf.save()
        bill = Bill(bill_file=bf, sim_id=row.num, period=row.per, amount=row.amount, contract_id=row.grp)
        bill.save()

    context = {'message': 'Все OK'}
    return render(request, 'mobile/access_sync.html', context)