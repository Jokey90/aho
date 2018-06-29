from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages


def penalty_list(request, show_all=False):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from td.models import Penalty

    page = request.GET.get('page', 1)
    if show_all:
        data = Penalty.objects.order_by('-date', 'driver')
    else:
        data = Penalty.objects.filter(payed=False).order_by('-date', 'driver')

    paginator = Paginator(data, 10)

    try:
        penalties = paginator.page(page)
    except PageNotAnInteger:
        penalties = paginator.page(1)
    except EmptyPage:
        penalties = paginator.page(paginator.num_pages)

    context = {
        'penalties': penalties,
        'show_all': show_all
    }

    return render(request, 'td/penalty/penalty_list.html', context)


def penalty_info(request, pid):
    from td.models import Penalty

    penalty = get_object_or_404(Penalty, id=pid)

    context = {
        'penalty': penalty
    }

    return render(request, 'td/penalty/penalty_info.html', context)


def penalty_new(request):
    from td.forms import PenaltyForm
    from django.middleware.csrf import rotate_token

    car = request.GET.get('car', None)
    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        form = PenaltyForm(initial={'car': car}, new=True)

        context = {'form': form}
        return render(request, 'td/penalty/penalty_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = PenaltyForm(request.POST, request.FILES, new=True)

        if form.is_valid():
            penalty = form.save()
            messages.success(request, 'штраф добавлен')
            if return_path == 'car_penalties':
                return redirect(to='td:car_penalties', cid=penalty.car.id)
            else:
                return redirect(to='td:penalty_info', pid=penalty.id)
        else:
            context = {'form': form}
            return render(request, 'td/penalty/penalty_new.html', context)


def penalty_edit(request, pid):
    from td.forms import PenaltyForm
    from td.models import Penalty
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        penalty = get_object_or_404(Penalty, id=pid)
        form = PenaltyForm(instance=penalty)
        context = {'form': form}
        return render(request, 'td/penalty/penalty_edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        penalty = get_object_or_404(Penalty, id=pid)
        form = PenaltyForm(request.POST, request.FILES, instance=penalty)

        if form.is_valid():
            form.save()
            messages.success(request, 'Запись изменена')
            if return_path == 'car_penalties':
                return redirect(to='td:car_penalties', cid=penalty.car.id)
            else:
                return redirect(to='td:penalty_info', pid=pid)
        else:
            context = {'form': form}
            return render(request, 'td/penalty/penalty_edit.html', context)


def penalty_delete(request, pid):
    from td.models import Penalty

    return_path = request.GET.get('return', None)
    item = get_object_or_404(Penalty, id=pid)
    item.delete()
    messages.success(request, 'Запись удалена')

    if return_path == 'car_penalties':
        return redirect(to='td:car_penalties', cid=item.car.id)
    else:
        return redirect(to='td:penalty_list')
