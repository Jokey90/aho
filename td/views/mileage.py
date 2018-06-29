from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.template import RequestContext
from django.contrib import messages


def mileage_list(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from td.models import Mileage

    mileages_list = Mileage.objects.order_by('-year', '-month').all()

    paginator = Paginator(mileages_list, 10)
    page = request.GET.get('page')

    try:
        mileages = paginator.page(page)
    except PageNotAnInteger:
        mileages = paginator.page(1)
    except EmptyPage:
        mileages = paginator.page(paginator.num_pages)

    context = {
        'mileages': mileages
    }

    return render(request, 'td/mileage/mileage_list.html', context)


def mileage_new(request):
    from td.forms import MileageForm
    from django.middleware.csrf import rotate_token
    from td.models import Mileage
    from datetime import date

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        car = request.GET.get('car', None)
        last_mileage = None
        last_mileage_data = Mileage.objects.filter(car_id=car).order_by('-year', '-month').first()
        if last_mileage_data:
            last_mileage = last_mileage_data.value

        form = MileageForm(initial={
            'car': car,
            'value': last_mileage,
            'year': date.today().year
        }, new=True)

        context = {'form': form}
        return render(request, 'td/mileage/mileage_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = MileageForm(request.POST, new=True)

        if form.is_valid():
            if Mileage.objects.filter(
                    year=form.cleaned_data['year'],
                    month=form.cleaned_data['month'],
                    car=form.cleaned_data['car']).count() > 0:
                messages.warning(request, 'Невозмоно добавить два значения пробега за один период')
                context = {'form': form}
                return render(request, 'td/mileage/mileage_new.html', context)
            else:
                mileage = form.save()
                messages.success(request, 'Пробег добавлен')
                if return_path == 'car_mileage':
                    return redirect(to='td:car_mileage', cid=mileage.car.id)
                else:
                    return redirect(to='td:mileage_info', mid=mileage.id)
        else:
            context = {'form': form}
            return render(request, 'td/mileage/mileage_new.html', context)


def mileage_info(request, mid):
    from td.models import Mileage

    mileage = get_object_or_404(Mileage, id=mid)

    context = {
        'mileage': mileage
    }

    return render(request, 'td/mileage/mileage_info.html', context)


def mileage_edit(request, mid):
    from td.models import Mileage
    from td.forms import MileageForm
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        mileage = get_object_or_404(Mileage, id=mid)
        form = MileageForm(instance=mileage)
        context = {'form': form}
        return render(request, 'td/mileage/mileage_edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        mileage = get_object_or_404(Mileage, id=mid)
        form = MileageForm(request.POST, instance=mileage)

        if form.is_valid():
            if Mileage.objects.filter(
                    year=form.cleaned_data['year'],
                    month=form.cleaned_data['month'],
                    car=form.cleaned_data['car']).exclude(id=mid).count() > 0:
                messages.warning(request, 'Невозмоно добавить два значения пробега за один период')
                context = {'form': form}
                return render(request, 'td/mileage/mileage_edit.html', context)
            else:
                form.save()
                messages.success(request, 'Пробег изменен')
                if return_path == 'car_mileage':
                    return redirect(to='td:car_mileage', cid=mileage.car.id)
                else:
                    return redirect(to='td:mileage_info', mid=mid)
        else:
            context = {'form': form}
            return render(request, 'td/mileage/mileage_edit.html', context)


def mileage_delete(request, mid):
    from td.models import Mileage

    return_path = request.GET.get('return', None)
    mileage = get_object_or_404(Mileage, id=mid)
    mileage.delete()
    messages.success(request, 'Пробег удален')

    if return_path == 'car_mileage':
        return redirect(to='td:car_mileage', cid=mileage.car.id)
    else:
        return redirect(to='td:mileage_list')