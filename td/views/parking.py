from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages


def parking_list(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from td.models import Parking

    page = request.GET.get('page', 1)
    parkings = Parking.objects.order_by('number').all()

    context = {
        'parkings': parkings
    }

    return render(request, 'td/parking/parking_list.html', context)


def parking_info(request, pid):
    from td.models import Parking

    parking = get_object_or_404(Parking, id=pid)

    context = {
        'parking': parking
    }

    return render(request, 'td/parking/parking_info.html', context)


def parking_new(request):
    from td.forms import ParkingForm
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        form = ParkingForm(new=True)

        context = {'form': form}
        return render(request, 'td/parking/parking_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = ParkingForm(request.POST, new=True)

        if form.is_valid():
            parking = form.save()
            messages.success(request, 'Парковочное место добавлено')
            return redirect(to='td:parking_info', pid=parking.id)
        else:
            context = {'form': form}
            return render(request, 'td/parking/parking_new.html', context)


def parking_edit(request, pid):
    from td.forms import ParkingForm
    from td.models import Parking
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        parking = get_object_or_404(Parking, id=pid)
        form = ParkingForm(instance=parking)
        context = {'form': form}
        return render(request, 'td/parking/parking_edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        parking = get_object_or_404(Parking, id=pid)
        form = ParkingForm(request.POST, instance=parking)

        if form.is_valid():
            form.save()
            messages.success(request, 'Запись изменена')
            return redirect(to='td:parking_info', pid=pid)
        else:
            context = {'form': form}
            return render(request, 'td/parking/parking_edit.html', context)


def parking_delete(request, pid):
    from td.models import Parking

    item = get_object_or_404(Parking, id=pid)
    item.delete()
    messages.success(request, 'Запись удалена')

    return redirect(to='td:parking_list')