from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages


def driver_list(request, show_inactive=False):
    from td.models import Driver, Proxy

    if show_inactive:
        drivers_list = Driver.objects.filter(active=False).order_by('emp__last_name', 'emp__first_name').all()
    else:
        drivers_list = Driver.objects.filter(active=True).order_by('emp__last_name', 'emp__first_name').all()

    drivers = []
    for driver in drivers_list:
        drivers.append({
            'driver': driver,
            'proxies': Proxy.objects.filter(driver=driver, active=True).all()
        })

    context = {
        'drivers': drivers,
        'show_inactive': show_inactive
    }

    return render(request, 'td/driver/driver_list.html', context)


def driver_info(request, did):
    from td.models import Driver, Proxy, Item

    driver = get_object_or_404(Driver, id=did)
    items = []
    proxies = []
    for item in Item.objects.filter(active=True):
        if item.current_owner() == driver:
            items.append(item)
    for proxy in Proxy.objects.filter(active=True):
        if proxy.current_owner() == driver:
            proxies.append(proxy)

    context = {
        'driver': driver,
        'proxies': proxies,
        'items': items
    }

    return render(request, 'td/driver/driver_info.html', context)


def driver_new(request):
    from td.forms import DriverForm
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        form = DriverForm(new=True)

        context = {'form': form}
        return render(request, 'td/driver/driver_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = DriverForm(request.POST, request.FILES, new=True)

        if form.is_valid():
            driver = form.save()
            messages.success(request, 'Водитель добавлен')
            return redirect(to='td:driver_info', did=driver.id)
        else:
            context = {'form': form}
            return render(request, 'td/driver/driver_new.html', context)


def driver_edit(request, did):
    from td.forms import DriverForm
    from td.models import Driver
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        driver = get_object_or_404(Driver, id=did)
        form = DriverForm(instance=driver)
        context = {'form': form}
        return render(request, 'td/driver/driver_edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        driver = get_object_or_404(Driver, id=did)
        form = DriverForm(request.POST, request.FILES, instance=driver)

        if form.is_valid():
            '''if len(request.FILES) == 1:
                if request.FILES['photo'].size > 1024 * 1024 * 10:
                    messages.error(request, 'Фото слишком большое')
                    context = {'form': form}
                    return render(request, 'td/driver/driver_edit.html', context)
                if request.FILES['photo'].content_type[0:5] != 'image':
                    messages.error(request, 'Неверный формат изображения')
                    context = {'form': form}
                    return render(request, 'td/driver/driver_edit.html', context)'''

            form.save()
            messages.success(request, 'Водитель изменен')
            return redirect(to='td:driver_info', did=did)
        else:
            context = {'form': form}
            return render(request, 'td/driver/driver_edit.html', context)


def driver_delete(request, did):
    from td.models import Driver

    driver = get_object_or_404(Driver, id=did)
    if driver.active:
        driver.active = False
        driver.save()
        messages.success(request, 'Водитель удален')
        return redirect(to='td:driver_list')
    else:
        driver.active = True
        driver.save()
        messages.success(request, 'Водитель восстановлен')
        return redirect(to='td:driver_list_inactive')