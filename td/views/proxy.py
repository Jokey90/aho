from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages


def proxy_list(request, show_inactive=False):
    from td.models import Proxy
    from datetime import date

    if show_inactive:
        proxies = Proxy.objects.filter(active=False).order_by('type', 'driver__emp__last_name').all()
    else:
        proxies = Proxy.objects.filter(active=True).order_by('type', 'driver__emp__last_name').all()

    context = {
        'proxies': proxies,
        'show_inactive': show_inactive,
        'today': date.today()
    }

    return render(request, 'td/proxy/proxy_list.html', context)


def proxy_info(request, pid):
    from td.models import Proxy, ProxyTracking

    proxy = get_object_or_404(Proxy, id=pid)
    tracking = ProxyTracking.objects.filter(proxy=proxy).order_by('-date')

    context = {
        'proxy': proxy,
        'tracking': tracking
    }

    return render(request, 'td/proxy/proxy_info.html', context)


def proxy_new(request):
    from td.forms import ProxyForm
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        car_id = request.GET.get('car', None)
        form = ProxyForm(initial={
            'car': car_id
        }, new=True)

        context = {'form': form}
        return render(request, 'td/proxy/proxy_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = ProxyForm(request.POST, request.FILES, new=True)

        if form.is_valid():
            proxy = form.save()
            messages.success(request, 'Доверенность добавлена')
            if return_path == 'car_proxies':
                return redirect(to='td:car_proxies', cid=proxy.car.id)
            else:
                return redirect(to='td:proxy_info', pid=proxy.id)
        else:
            context = {'form': form}
            return render(request, 'td/proxy/proxy_new.html', context)


def proxy_edit(request, pid):
    from td.forms import ProxyForm
    from td.models import Proxy
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        proxy = get_object_or_404(Proxy, id=pid)
        form = ProxyForm(instance=proxy)
        context = {'form': form}
        return render(request, 'td/proxy/proxy_edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        proxy = get_object_or_404(Proxy, id=pid)
        form = ProxyForm(request.POST, request.FILES, instance=proxy)

        if form.is_valid():
            form.save()
            messages.success(request, 'Доверенность изменена')
            if return_path == 'car_proxies':
                return redirect(to='td:car_proxies', cid=proxy.car.id)
            elif return_path == 'proxy_list':
                return redirect(to='td:proxy_list')
            else:
                return redirect(to='td:proxy_info', pid=pid)
        else:
            context = {'form': form}
            return render(request, 'td/proxy/proxy_edit.html', context)


def proxy_delete(request, pid):
    from td.models import Proxy

    proxy = get_object_or_404(Proxy, id=pid)
    return_path = request.GET.get('return', None)
    if proxy.active:
        proxy.active = False
        proxy.save()
        messages.success(request, 'Доверенность удалена')
        if return_path == 'car_proxies':
            return redirect(to='td:car_proxies', cid=proxy.car.id)
        else:
            return redirect(to='td:proxy_list')
    else:
        proxy.active = True
        proxy.save()
        messages.success(request, 'Доверенность восстановлена')
        return redirect(to='td:proxy_list_inactive')
