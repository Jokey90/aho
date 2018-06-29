from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404


def car_list(request, show_inactive=False):
    from td.models.car import Car
    from td.models import Proxy
    from datetime import date

    if show_inactive:
        cars_list = Car.objects.filter(active=False).order_by('name', 'number').all()
    else:
        cars_list = Car.objects.filter(active=True).order_by('name', 'number').all()

    cars = []
    for car in cars_list:
        temp = {
            'id': car.id,
            'name': car.name,
            'owner': car.owner,
            'number': car.number,
            'active': car.active,
            'drivers': [],
            'warnings': []
        }
        for driver in Proxy.objects.filter(car=car, end_date__gte=date.today(), start_date__lte=date.today(), type=0).all():
            temp['drivers'].append({
                'id': driver.driver_id,
                'name': driver.driver.emp.short_name(),
                'start_date': driver.start_date,
                'end_date': driver.end_date
            })
            '''if driver.end_date-timedelta(days=30) <= date.today():
                temp['warnings'].append('Доверенность '+driver.driver.emp.short_name()+' закончится менее чем через месяц')'''

        cars.append(temp)

    context = {
        'cars': cars,
        'show_inactive': show_inactive
    }

    return render(request, 'td/car/car_list.html', context)


def car_new(request):
    from td.forms import CarNewForm
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        form = CarNewForm()

        context = {'form': form}
        return render(request, 'td/car/car_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = CarNewForm(request.POST)

        if form.is_valid():
            car = form.save()
            messages.success(request, 'Автомобиль добавлен')
            return redirect(to='td:car_list')
            #return redirect(to='td:car_info', cid=car.id)
        else:
            context = {'form': form}
            return render(request, 'td/car/car_new.html', context)


def car_info(request, cid, block='info'):
    from td.models import Car

    car = get_object_or_404(Car, id=cid)

    context = {
        'car': car
    }

    return render(request, 'td/car/car_'+block+'.html', context)


def car_proxies(request, cid):
    from td.models import Car, Proxy
    from datetime import date

    car = get_object_or_404(Car, id=cid)
    proxies = Proxy.objects.filter(car=car, active=True).all().order_by('type', 'end_date')

    context = {
        'car': car,
        'proxies': proxies,
        'today': date.today()
    }
    return render(request, 'td/car/car_proxies.html', context)


def car_accidents(request, cid):
    from td.models import Car, Accident
    from datetime import date

    car = get_object_or_404(Car, id=cid)
    accidents = Accident.objects.filter(car=car).all().order_by('-date')

    context = {
        'car': car,
        'accidents': accidents,
        'today': date.today()
    }
    return render(request, 'td/car/car_accidents.html', context)


def car_penalties(request, cid):
    from td.models import Car, Penalty
    from datetime import date

    car = get_object_or_404(Car, id=cid)
    penalties = Penalty.objects.filter(car=car).all().order_by('-date').all()

    context = {
        'car': car,
        'penalties': penalties,
        'today': date.today()
    }
    return render(request, 'td/car/car_penalties.html', context)


def car_to(request, cid):
    from td.models import Car, TO

    car = get_object_or_404(Car, id=cid)

    to_list = TO.objects.filter(car=car).order_by('-date')

    context = {
        'car': car,
        'to_list': to_list
    }

    return render(request, 'td/car/car_to.html', context)


def car_docs(request, cid):
    from td.models import Car, Item

    car = get_object_or_404(Car, id=cid)
    items = Item.objects.filter(car=car, active=1, type__in=[t[1] for t in Item.TYPES if t[0]=='doc']).all().order_by('type')

    context = {
        'car': car,
        'items': items
    }
    return render(request, 'td/car/car_docs.html', context)


def car_ensurance(request, cid):
    from td.models import Car, Item

    car = get_object_or_404(Car, id=cid)
    items = Item.objects.filter(car=car, active=1, type__in=[t[1] for t in Item.TYPES if t[0] == 'ensurance']).all().order_by('type')

    context = {
        'car': car,
        'items': items
    }
    return render(request, 'td/car/car_ensurance.html', context)


def car_keys(request, cid):
    from td.models import Car, Item

    car = get_object_or_404(Car, id=cid)
    items = Item.objects.filter(car=car, active=1, type__in=[t[1] for t in Item.TYPES if t[0]=='key']).all().order_by('type')

    context = {
        'car': car,
        'items': items
    }
    return render(request, 'td/car/car_keys.html', context)


def car_edit(request, cid, block='info'):
    from td.models import Car
    from td.forms import CarEditInfoForm, CarEditTiresForm
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        car = get_object_or_404(Car, id=cid)
        if block == 'info':
            form = CarEditInfoForm(instance=car)
        elif block == 'tires':
            form = CarEditTiresForm(instance=car)
        context = {
            'form': form,
            'car': car
        }
        return render(request, 'td/car/car_edit_'+block+'.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        car = get_object_or_404(Car, id=cid)
        form = None

        if block == 'info':
            form = CarEditInfoForm(request.POST, request.FILES, instance=car)
        elif block == 'tires':
            form = CarEditTiresForm(request.POST, request.FILES, instance=car)

        if form.is_valid():
            form.save()
            messages.success(request, 'Автомобиль изменен')
            return redirect(to='td:car_'+block, cid=cid)
        else:
            context = {
                'form': form,
                'car': car
            }
            print(form.errors)
            return render(request, 'td/car/car_edit_'+block+'.html', context)


def car_delete(request, cid):
    from td.models import Car

    car = get_object_or_404(Car, id=cid)
    if car.active:
        car.active = False
        car.save()
        messages.success(request, 'Автомобиль удален')
        return redirect(to='td:car_list')
    else:
        car.active = True
        car.save()
        messages.success(request, 'Автомобиль восстановлен')
        return redirect(to='td:car_list_inactive')


def car_mileage(request, cid):
    from td.models import Car, Mileage

    car = get_object_or_404(Car, id=cid)

    mileage_list = Mileage.objects.with_periods().filter(car=car).order_by('-year', '-month').all()

    context = {
        'car': car,
        'mileage_list': mileage_list,
    }

    return render(request, 'td/car/car_mileage.html', context)


def car_expenses(request, cid):
    from td.models import Car, Expense
    from main.structures import MONTHS
    from django.db.models import Sum

    car = get_object_or_404(Car, id=cid)

    expenses = []
    for exp in Expense.objects.filter(car=car, active=True).order_by('-date').all():
        expenses.append({
            'id': exp.id,
            'year': exp.date.year,
            'month': exp.date.month,
            'month_name': MONTHS[exp.date.month-1][1],
            'driver': exp.driver,
            'budget_subitem': exp.budget_subitem,
            'amount': exp.amount,
            'active': exp.active,
            'sum': Expense.objects.filter(
                car=car,
                active=True,
                date__year=exp.date.year,
                date__month=exp.date.month).aggregate(Sum('amount'))['amount__sum']
        })

    context = {
        'car': car,
        'expenses': expenses
    }

    return render(request, 'td/car/car_expenses.html', context)


def car_mileage_graph(request, cid, year=datetime.today().year):
    from td.models import Car, Mileage
    from main.structures import MONTHS
    from json import dumps
    from django.urls import reverse

    car = get_object_or_404(Car, id=cid)

    mileages = []
    for m in MONTHS:
        month = m[0]
        mileage = Mileage.objects.filter(car=car, year=year, month=month).all()
        link = None
        if len(mileage)>0:
            value = float(mileage[0].value)
            link = reverse('td:mileage_info', args=(mileage[0].id,))
            diff = None
            for last in Mileage.objects.raw('SELECT TOP 1 id, value FROM td_mileage '
                                            'WHERE car_id=%s and (year*100+month)<%s*100+%s ORDER BY year desc, month desc',
                                            (car.id, year, month)):
                diff = value - float(last.value)

        else:
            value = None
            diff = None

        mileages.append({
            'month': m[1],
            'value': value,
            'diff': diff,
            'link': link
        })

    years = []
    for row in Mileage.objects.filter(car=car).order_by('year').all():
        if row.year not in years:
            years.append(row.year)

    context = {
        'car': car,
        'mileages': dumps(mileages),
        'year': int(year),
        'years': years
    }

    return render(request, 'td/car/car_mileage.html', context)