from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.middleware.csrf import rotate_token


def limit_report_form(request):
    from mobile.forms import LimitReportForm

    if request.method == 'POST':
        form = LimitReportForm(request.POST)

        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']

            return redirect(to='mobile:limit_report', month=month, year=year)
        else:
            context = {'form': form}
            return render(request, 'mobile/report/limit_form.html', context)
    else:
        form = LimitReportForm()
        context = {'form': form}
        return render(request, 'mobile/report/limit_form.html', context)


def limit_report(request, year, month):
    from mobile.models import Sim
    from main.models import Employee

    year = int(year)
    month = int(month)

    sims_past = Sim.objects.with_month_stats(year-1, month)
    sims_now = Sim.objects.with_month_stats(year, month)
    emps = dict()
    for emp in Employee.objects.all():
        emps[emp.id] = emp.short_name()

    sim_nums = list(set([s.number for s in sims_past]) | set([s.number for s in sims_now]))

    table = []
    for num in sorted(sim_nums):
        row = {
            'number': num,
            'bill_past': 0,
            'limit_past': None,
            'bill_now': 0,
            'limit_now': None
        }
        for sim in filter(lambda x: x.number == num, sims_past):
            if sim.owner_id:
                row['owner_past'] = emps[sim.owner_id]
            row['bill_past'] = sim.bill_amount
            row['limit_past'] = None if sim.limit_infinite else sim.limit
        for sim in filter(lambda x: x.number == num, sims_now):
            if sim.owner_id:
                row['owner_now'] = emps[sim.owner_id]
            row['bill_now'] = sim.bill_amount
            row['limit_now'] = None if sim.limit_infinite else sim.limit
        if row['bill_now'] or row['bill_past']:
            table.append(row)

    context = {
        'year': year,
        'year_past': year-1,
        'month': month,
        'table': table
    }
    return render(request, 'mobile/report/limit.html', context)
