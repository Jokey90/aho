from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.middleware.csrf import rotate_token


def limit_new(request, uid=None):
    from django.middleware.csrf import rotate_token
    from mobile.forms import LimitForm

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        form = LimitForm(initial={'sim': uid})
        context = {'form': form}
        return render(request, 'mobile/limit/new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = LimitForm(request.POST)

        if form.is_valid():
            limit = form.save()
            messages.success(request, 'SIM-карта передана')
            return redirect(to='mobile:sim_limits', uid=limit.sim_id)
        else:
            context = {'form': form}
            return render(request, 'mobile/limit/new.html', context)


def limit_edit(request, uid):
    from mobile.models import Limit
    from mobile.forms import LimitForm

    limit = get_object_or_404(Limit, id=uid)
    if request.method == 'GET':
        form = LimitForm(instance=limit)
        context = {'form': form}
        return render(request, 'mobile/limit/edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = LimitForm(request.POST, instance=limit)
        if form.is_valid():
            limit = form.save()
            messages.success(request, 'Изменения применены')
            return redirect(to='mobile:sim_limits', uid=limit.sim.id)
        else:
            context = {'form': form}
            return render(request, 'mobile/limit/edit.html', context)


def limit_delete(request, uid):
    from mobile.models import Limit

    limit = get_object_or_404(Limit, id=uid)

    sim_id = limit.sim_id

    limit.delete()
    messages.warning(request, 'Запись удалена')

    return redirect(to='mobile:sim_limits', uid=sim_id)