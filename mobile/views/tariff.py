from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.middleware.csrf import rotate_token


def tariff_new(request):
    from mobile.forms import TariffForm

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        form = TariffForm()
        context = {'form': form}
        return render(request, 'mobile/tariff/new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = TariffForm(request.POST)

        if form.is_valid():
            tariff = form.save()
            messages.success(request, 'Тариф добавлен')
            return redirect(to='mobile:tariff_info', uid=tariff.id)
        else:
            context = {'form': form}
            return render(request, 'mobile/tariff/new.html', context)


def tariff_info(request, uid):
    from mobile.models import Tariff

    tariff = get_object_or_404(Tariff, id=uid)
    context = {'tariff': tariff}
    return render(request, 'mobile/tariff/info.html', context)


def tariff_edit(request, uid):
    from mobile.models import Tariff
    from mobile.forms import TariffForm

    tariff = get_object_or_404(Tariff, id=uid)
    if request.method == 'GET':
        form = TariffForm(instance=tariff)
        context = {'form': form}
        return render(request, 'mobile/tariff/edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = TariffForm(request.POST, instance=tariff)
        if form.is_valid():
            tariff = form.save()
            messages.success(request, 'Изменения применены')
            return redirect(to='mobile:tariff_list')
        else:
            context = {'form': form}
            return render(request, 'mobile/tariff/edit.html', context)


def tariff_list(request):
    from mobile.models import Tariff

    tariffs = Tariff.objects.order_by('name')

    context = {
        'tariffs': tariffs
    }

    return render(request, 'mobile/tariff/list.html', context)


def tariff_delete(request, uid):
    from mobile.models import Tariff

    tariff = get_object_or_404(Tariff, id=uid)
    sims = tariff.sim_set.count()
    if sims == 0:
        tariff.delete()
        messages.warning(request, 'Объект удален')
    else:
        messages.warning(request, 'Невозможно удалить. Тариф используется '+str(sims)+' SIM-картами.')

    return redirect(to='mobile:tariff_list')
