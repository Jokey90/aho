from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages


def expense_list(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from td.models import Expense

    page = request.GET.get('page', 1)

    if request.GET.get('all', 0):
        data = Expense.objects.all().order_by('-date')
    else:
        data = Expense.objects.filter(active=True).all().order_by('-date')

    paginator = Paginator(data, 25)

    try:
        expenses = paginator.page(page)
    except PageNotAnInteger:
        expenses = paginator.page(1)
    except EmptyPage:
        expenses = paginator.page(paginator.num_pages)

    context = {
        'expenses': expenses
    }

    return render(request, 'td/expense/expense_list.html', context)


def expense_info(request, eid):
    from td.models import Expense

    expense = get_object_or_404(Expense, id=eid)

    context = {
        'expense': expense
    }

    return render(request, 'td/expense/expense_info.html', context)


def expense_new(request):
    from td.forms import ExpenseForm
    from django.middleware.csrf import rotate_token
    from td.models import Proxy, BudgetItem, BudgetSubitem
    from datetime import date
    from json import dumps

    if request.method == 'GET':
        car = request.GET.get('car', None)
        driver_proxy = Proxy.objects.filter(
            car_id=car,
            start_date__lte=date.today(),
            end_date__gte=date.today(),
            type=0
        ).order_by('start_date').first()

        if driver_proxy is not None:
            driver = driver_proxy.driver_id
        else:
            driver = None

        drivers = []
        for d in Proxy.objects.filter(end_date__gte=date.today(), type=0).all():
            drivers.append({
                'car_id': d.car_id,
                'driver_id': d.driver_id,
                'driver_name': d.driver.short_name()
            })

        budget_selector = ''
        for item in BudgetItem.objects.all():
            budget_selector += '<option value disabled>'+item.name+'</option>'
            for subitem in BudgetSubitem.objects.filter(parent_item=item).all():
                budget_selector += '<option value="'+str(subitem.id)+'">&nbsp;&nbsp;&nbsp;&nbsp;'+str(subitem.name)+'</option>'

        form = ExpenseForm(initial={'car': car, 'driver': driver})

        context = {
            'form': form,
            'drivers': dumps(drivers),
            'budget_selector': budget_selector
        }
        return render(request, 'td/expense/expense_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save()
            messages.success(request, 'Расход добавлен')
            return redirect(to='td:expense_info', eid=expense.id)
        else:
            context = {'form': form}
            return render(request, 'td/expense/expense_new.html', context)


def expense_edit(request, eid):
    from td.forms import ExpenseForm
    from td.models import Expense
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        expense = get_object_or_404(Expense, id=eid)
        form = ExpenseForm(instance=expense)
        context = {'form': form}
        return render(request, 'td/expense/expense_edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        expense = get_object_or_404(Expense, id=eid)
        form = ExpenseForm(request.POST, instance=expense)

        if form.is_valid():
            form.save()
            messages.success(request, 'Запись изменена')
            return redirect(to='td:expense_info', eid=eid)
        else:
            context = {'form': form}
            return render(request, 'td/expense/expense_edit.html', context)


def expense_delete(request, eid):
    from td.models import Expense

    item = get_object_or_404(Expense, id=eid)
    if item.active:
        item.active = False
        messages.success(request, 'Запись удалена')
    else:
        item.active = True
        messages.success(request, 'Запись восстановлена')
    item.save()


    return redirect(to='td:expense_list')