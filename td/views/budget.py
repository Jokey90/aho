from django.shortcuts import render


def budget_list(request):
    from datetime import date
    from td.models import BudgetItem, BudgetSubitem, BudgetValue
    from django.db.models import Sum

    year = request.GET.get('year', date.today().year)

    rows = []
    subrows = []
    totals = [0,0,0,0,0,0,0,0,0,0,0,0]

    for item in BudgetItem.objects.all():
        row = {
            'id': item.id,
            'name': item.name,
            'values': [0,0,0,0,0,0,0,0,0,0,0,0]
        }
        for subitem in BudgetSubitem.objects.filter(parent_item=item).all():
            subrow = {
                'id': subitem.id,
                'parent_id': item.id,
                'name': subitem.name,
                'values': [0,0,0,0,0,0,0,0,0,0,0,0]
            }
            for month in range(1, 13):
                s = BudgetValue.objects.filter(year=year, month=month, budget_subitem=subitem).all().aggregate(Sum('amount'))['amount__sum']
                if s is not None:
                    subrow['values'][month-1] += s
                    row['values'][month - 1] += s
                    totals[month-1] += s
            subrow['sum'] = sum(subrow['values'])
            subrows.append(subrow)
        row['sum'] = sum(row['values'])
        rows.append(row)
    rows.append({
        'level': 0,
        'name': 'Итого',
        'values': totals,
        'sum': sum(totals)
    })

    context = {
        'rows': rows,
        'subrows': subrows,
        'year': year
    }

    return render(request, 'td/budget/budget_list.html', context)


def budget_details(request, year, month, item):
    from td.models import BudgetValue
    from main.structures import MONTHS

    data =  BudgetValue.objects.filter(year=year, month=month, budget_subitem_id=item).all().order_by('car')

    context = {
        'data': data,
        'year': year,
        'month': MONTHS[int(month)][1]
    }

    return render(request, 'td/budget/budget_details.html', context)


def budget_subitem_details(request, year, item):
    from td.models import BudgetValue, Car, BudgetSubitem
    from django.db.models import Sum

    data = []
    totals = [0,0,0,0,0,0,0,0,0,0,0,0]
    for car in Car.objects.filter(active=True).all():
        values = [0,0,0,0,0,0,0,0,0,0,0,0]
        for month in range(1,13):
            budget = BudgetValue.objects.filter(car=car, year=year, month=month, budget_subitem_id=item).all().aggregate(Sum('amount'))['amount__sum']
            if budget is not None:
                values[month-1] += budget
                totals[month-1] += budget
        values.append(sum(values))
        data.append({
            'car': car,
            'values': values
        })

    totals.append(sum(totals))

    context = {
        'name': BudgetSubitem.objects.get(id=item).name,
        'data': data,
        'year': year,
        'totals': totals
    }

    return render(request, 'td/budget/budget_subitem_details.html', context)