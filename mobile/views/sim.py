from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.middleware.csrf import rotate_token


def sim_list(request, show_inactive=False):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from mobile.models import Sim
    from mobile.forms import SimSearchForm
    import re

    page = request.GET.get('page', 1)
    search_text = re.sub('[^а-яА-Яa-zA-Z]', '', request.GET.get('search', '').lower())
    search_num = re.sub('[^0-9]', '', request.GET.get('search', ''))

    form = SimSearchForm(initial={'search': request.GET.get('search', '')})

    initial_recordset = Sim.objects.with_current_stats()

    if show_inactive:
        temp_data = [x for x in initial_recordset if x.active is False]
    else:
        temp_data = [x for x in initial_recordset if x.active is True]

    data = []
    for sim in temp_data:
        if len(search_num) > 0 and search_num in sim.number:
            data.append(sim)
            continue
        if len(search_text) > 0 and search_text in re.sub('[^а-яА-Яa-zA-Z]', '', sim.owner_name.lower()):
            data.append(sim)
            continue

        if search_text == '' and search_num == '':
            data.append(sim)
            continue

    paginator = Paginator(data, 25)

    try:
        sims = paginator.page(page)
    except PageNotAnInteger:
        sims = paginator.page(1)
    except EmptyPage:
        sims = paginator.page(paginator.num_pages)

    context = {
        'sims': sims,
        'show_inactive': show_inactive,
        'search_form': form
    }

    return render(request, 'mobile/sim/list.html', context)


def sim_new(request):
    from django.middleware.csrf import rotate_token
    from mobile.forms import SimForm

    return_path = request.GET.get('return', None)
    sim_number = request.GET.get('num', None)
    if request.method == 'GET':
        form = SimForm(initial={'number': sim_number})
        context = {'form': form}
        return render(request, 'mobile/sim/new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = SimForm(request.POST)

        if form.is_valid():
            sim = form.save()
            messages.success(request, 'SIM-карта добавлена')
            return redirect(to='mobile:sim_list')
        else:
            context = {'form': form}
            return render(request, 'mobile/sim/new.html', context)


def sim_generate(request, bill_id):
    from mobile.models import Sim, Bill

    bill = get_object_or_404(Bill, id=bill_id)
    sim = Sim(number=bill.number, active=True)
    sim.save()
    bill.sim = sim
    bill.save()

    return redirect(to='mobile:bill_file_info', uid=bill.bill_file_id)


def sim_info(request, uid, module='info'):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from mobile.models import Sim, Transition, Bill, Limit

    sim = get_object_or_404(Sim, id=uid)
    context = {'sim': sim}

    if module == 'info':
        return render(request, 'mobile/sim/info.html', context)
    elif module == 'transitions':
        context['transitions'] = Transition.objects.filter(sim=sim).order_by('-date')
        return render(request, 'mobile/sim/transitions.html', context)
    elif module == 'bills':

        page = request.GET.get('page', 1)
        data = Bill.objects.filter(sim=sim).order_by('-period')
        paginator = Paginator(data, 12)

        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)

        context['bills'] = bills
        return render(request, 'mobile/sim/bills.html', context)
    elif module == 'limits':
        context['limits'] = Limit.objects.filter(sim=sim).order_by('-date')
        return render(request, 'mobile/sim/limits.html', context)


def sim_bills_chart(request, uid):
    from datetime import date
    from json import dumps
    from django.db import connection
    from mobile.models import Sim
    from main.forms import YearSelectForm

    year = request.GET.get('year', date.today().year)

    form = YearSelectForm(initial={'year': year})

    sim = get_object_or_404(Sim, id=uid)

    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT
                b.period as date,
                b.amount,
                coalesce((SELECT TOP 1 amount FROM mobile_limit WHERE date<=b.period and sim_id=b.sim_id ORDER BY date DESC),0) as limit_amount
            FROM
                mobile_bill as b
            WHERE
                b.sim_id=%s and year(b.period)=%s
            ORDER BY
                b.period ASC
        ''', (uid, year))

        data = []
        for row in cursor.fetchall():
            data.append({
                'date': row[0].isoformat(),
                'amount': row[1],
                'limit': row[2]
            })

        context = {
            'sim': sim,
            'data': dumps(data),
            'form': form
        }

        return render(request, 'mobile/sim/bills_chart.html', context)


def sim_edit(request, uid):
    from mobile.models import Sim
    from mobile.forms import SimForm

    sim = get_object_or_404(Sim, id=uid)
    if request.method == 'GET':
        form = SimForm(instance=sim)
        context = {'form': form}
        return render(request, 'mobile/sim/edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = SimForm(request.POST, instance=sim)
        if form.is_valid():
            form.save()
            messages.success(request, 'SIM-карта изменена')
            return redirect(to='mobile:sim_info', uid=sim.id)
        else:
            context = {'form': form}
            return render(request, 'mobile/sim/edit.html', context)


def sim_delete(request, uid):
    from mobile.models import Sim

    sim = get_object_or_404(Sim, id=uid)

    if sim.active:
        sim.active = False
        messages.warning(request, 'SIM-карта удалена')
    else:
        sim.active = True
        messages.warning(request, 'SIM-карта восстановлена')
    sim.save()
    if request.GET.get('return', '') == 'sim_info':
        return redirect(to='mobile:sim_info', uid=sim.id)
    else:
        return redirect(to='mobile:sim_list')
