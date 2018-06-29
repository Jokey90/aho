from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.middleware.csrf import rotate_token


def general_report_form(request):
    from mobile.forms import GeneralReportForm

    if request.method == 'POST':
        form = GeneralReportForm(request.POST)

        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']

            return redirect(to='mobile:general_report', month=month, year=year)
        else:
            context = {'form': form}
            return render(request, 'mobile/report/general_form.html', context)
    else:
        form = GeneralReportForm()
        context = {'form': form}
        return render(request, 'mobile/report/general_form.html', context)


def walk_deps_tree(lst, res=[], root=None, level=0, top_parent_id=None):
    for item in lst:
        if item.parent_department_id == root:
            item.level = level
            item.levels = range(level)
            if level == 0:
                item.top_parent_id = item.id
            else:
                item.top_parent_id = top_parent_id
            res.append(item)
            walk_deps_tree(lst, res, root=item.id, level=level + 1, top_parent_id=item.top_parent_id)
    return res


def general_report(request, year, month):
    from main.models import Department, Employee
    from mobile.models import Bill, Sim
    from django.db import connection

    deps = walk_deps_tree(Department.objects.all().order_by('division', 'id'), [])

    emps = dict()
    for emp in Employee.objects.all():
        emps[emp.id] = {
            'name': emp.short_name(),
            'dep': emp.department_id
        }

    bills = Bill.objects.with_sim_details(year, month)

    table = []
    for dep in deps:
        for bill in bills:
            emp = emps[bill.sim_owner_id]
            if emp['dep'] == dep.id:
                row = {
                    'dep_id': dep.id,
                    'dep_name': dep.name,
                    'dep_level': dep.level,
                    'dep_levels': dep.levels,
                    'top_parent_id': dep.top_parent_id,
                    'emp': emp['name'],
                    'number': bill.number,
                    'contract': bill.contract_name,
                    'amount': bill.amount,
                    'amount_nonds': bill.amount / 1.18,
                    'totals': 0
                }
                if bill.sim_limit_infinite:
                    row['limit'] = 'Безлимит'
                    row['economy'] = 0
                    row['exceed'] = 0
                else:
                    row['limit'] = bill.sim_limit
                    if bill.sim_limit >= bill.amount:
                        row['economy'] = bill.sim_limit - bill.amount
                        row['exceed'] = 0
                    else:
                        row['economy'] = 0
                        row['exceed'] = bill.amount - bill.sim_limit
                table.append(row)

    dep_totals = []
    for dep in deps:
        row = {'totals': 1}
        row['dep_id'] = dep.id
        row['dep_name'] = dep.name
        row['dep_level'] = dep.level
        row['dep_levels'] = dep.levels
        row['dep_limit'] = sum([x['limit'] for x in table if x['dep_id'] == dep.id and x['limit'] != 'Безлимит'])
        row['dep_amount'] = sum([x['amount'] for x in table if x['dep_id'] == dep.id])
        row['dep_amount_nonds'] = row['dep_amount'] / 1.18
        row['dep_economy'] = sum([x['economy'] for x in table if x['dep_id'] == dep.id])
        row['dep_exceed'] = sum([x['exceed'] for x in table if x['dep_id'] == dep.id])

        if dep.level == 0:
            row['top_dep_limit'] = sum([x['limit'] for x in table if x['top_parent_id'] == dep.id and x['limit'] != 'Безлимит'])
            row['top_dep_amount'] = sum([x['amount'] for x in table if x['top_parent_id'] == dep.id])
            row['top_dep_amount_nonds'] = row['top_dep_amount'] / 1.18
            row['top_dep_economy'] = sum([x['economy'] for x in table if x['top_parent_id'] == dep.id])
            row['top_dep_exceed'] = sum([x['exceed'] for x in table if x['top_parent_id'] == dep.id])

        dep_totals.append(row)

    i = 0
    dep_id = None
    while i < len(table):
        if table[i]['dep_id'] != dep_id:
            dep_id = table[i]['dep_id']
            for row in dep_totals:
                if row['dep_id'] == dep_id:
                    table.insert(i, row)
                    i += 1
            if dep.level == 0:
                pass

    context = {
        'year': year,
        'month': month,
        'table': table
    }

    msg = 'Queries: ' + str(len(connection.queries)) + '\n' + 'Time: ' + str(
        round(sum([float(x['time']) for x in connection.queries]), 3)) + ' seconds'
    messages.debug(request, msg)
    return render(request, 'mobile/report/general.html', context)
