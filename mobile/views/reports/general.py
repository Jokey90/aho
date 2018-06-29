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


def general_report(request, year, month):
    from main.models import Department, Employee, Group
    from mobile.models import Bill, Budget, Contract
    from datetime import datetime

    t0 = datetime.now()

    def create_deps_tree(lst, root=None, level=0):
        res = []
        for item in lst:
            if item.parent_department_id == root:
                row = {
                    'level': level,
                    'levels_range': range(level),
                    'dep_id': item.id,
                    'dep_name': item.name,
                    'division_id': item.division,
                    'children': create_deps_tree(lst, root=item.id, level=level + 1)
                }
                res.append(row)
        return res

    def process_dep(dep, bills, emps):
        res = []
        for bill in bills:
            emp = emps[bill.sim_owner_id]
            if emp['dep_id'] == dep['dep_id']:
                row = {
                    'emp': emp['name'],
                    'group_id': emp['group_id'],
                    'group_name': emp['group_name'],
                    'number': bill.number,
                    'contract': bill.contract_name,
                    'amount': bill.amount,
                    'amount_nonds': bill.amount / 1.18
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
                res.append(row)
        return res

    def walk_deps_tree(deps, bills, emps):
        for dep in deps:
            dep['rows'] = process_dep(dep, bills, emps)
            walk_deps_tree(dep['children'], bills, emps)
            dep['totals'] = {
                'limit': sum([x['limit'] for x in dep['rows'] if x['limit'] != 'Безлимит']),
                'amount': sum([x['amount'] for x in dep['rows']]),
                'amount_nonds': sum([x['amount_nonds'] for x in dep['rows']]),
                'economy': sum([x['economy'] for x in dep['rows']]),
                'exceed': sum([x['exceed'] for x in dep['rows']]),
            }
            dep['totals_sum'] = {
                'limit': sum([x['totals_sum']['limit'] for x in dep['children']])+dep['totals']['limit'],
                'amount': sum([x['totals_sum']['amount'] for x in dep['children']])+dep['totals']['amount'],
                'amount_nonds': sum([x['totals_sum']['amount_nonds'] for x in dep['children']])+dep['totals']['amount_nonds'],
                'economy': sum([x['totals_sum']['economy'] for x in dep['children']])+dep['totals']['economy'],
                'exceed': sum([x['totals_sum']['exceed'] for x in dep['children']])+dep['totals']['exceed'],
            }

    deps = create_deps_tree(Department.objects.all().order_by('division', 'id'))

    totals_div = dict()

    groups = dict()
    for g in Group.objects.all():
        groups[g.id] = g.name

    contracts = dict()
    for c in Contract.objects.all():
        contracts[c.id] = c.name

    divisions = dict()
    for d in Department.DIVISIONS:
        divisions[d[0]] = d[1]
        totals_div[d[0]] = {
            'name': d[1],
            'values': {
                'limit': 0,
                'amount': 0,
                'amount_nonds': 0,
                'economy': 0,
                'exceed': 0
            },
            'budget': {
                'amount': 0,
                'economy': 0,
                'exceed': 0
            }
        }
        if Budget.objects.filter(year=year, division=d[0]).exists():
            totals_div[d[0]]['budget']['amount'] = Budget.objects.filter(year=year, division=d[0]).first().amount

    emps = dict()
    for emp in Employee.objects.all():
        emps[emp.id] = {
            'name': emp.short_name(),
            'dep_id': emp.department_id,
            'group_id': emp.group_id or 2,
            'group_name': groups[emp.group_id or 2]
        }

    bills = Bill.objects.with_sim_details(year, month)

    walk_deps_tree(deps, bills, emps)

    for dep in deps:
        totals_div[dep['division_id']]['values']['limit'] += dep['totals_sum']['limit']
        totals_div[dep['division_id']]['values']['amount'] += dep['totals_sum']['amount']
        totals_div[dep['division_id']]['values']['amount_nonds'] += dep['totals_sum']['amount_nonds']
        totals_div[dep['division_id']]['values']['economy'] += dep['totals_sum']['economy']
        totals_div[dep['division_id']]['values']['exceed'] += dep['totals_sum']['exceed']

    for row in totals_div.values():
        if row['budget']['amount'] >= row['values']['amount']:
            row['budget']['economy'] = row['budget']['amount'] - row['values']['amount']
        else:
            row['budget']['exceed'] = row['values']['amount'] - row['budget']['amount']

    totals = []
    for g_id, g_name in groups.items():
        row = [g_name]
        row_sum = 0
        for c_id, c_name in contracts.items():
            val = 0
            for bill in bills:
                if bill.contract_id == c_id and emps[bill.sim_owner_id]['group_id'] == g_id:
                    val += bill.amount
            row.append(val)
            row_sum += val
        row.append(row_sum)
        totals.append(row)

    sums_row = ['Итого']
    sums_row_sum = 0
    for c_id, c_name in contracts.items():
        val = 0
        for bill in bills:
            if bill.contract_id == c_id:
                val += bill.amount
        sums_row.append(val)
        sums_row_sum += val
    sums_row.append(sums_row_sum)
    totals.append(sums_row)

    context = {
        'year': year,
        'month': month,
        'deps': deps,
        'totals_div': totals_div,
        'totals': totals,
        'contracts': contracts
    }
    return render(request, 'mobile/report/general.html', context)
