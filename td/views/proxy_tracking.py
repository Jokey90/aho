from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib import messages


def proxy_tracking_new(request, pid):
    from td.models import Proxy
    from td.forms import ProxyMoveForm
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    proxy = get_object_or_404(Proxy, id=pid)

    if request.method == 'GET':
        form = ProxyMoveForm(initial={'proxy': proxy}, new=True)
        context = {'form': form}
        return render(request, 'td/proxy_tracking/proxy_tracking_new.html', context)

    elif request.method == 'POST':
        rotate_token(request)
        form = ProxyMoveForm(request.POST, new=True)

        if form.is_valid():
            track = form.save(commit=False)
            track.added_by = request.user
            track.save()
            messages.success(request, 'Объект передан')
            if return_path == 'car_proxies':
                return redirect(to='td:car_proxies', cid=track.proxy.car.id)
            elif return_path == 'proxy_list':
                return redirect(to='td:proxy_list')
            else:
                return redirect(to='td:proxy_info', pid=track.proxy.id)
        else:
            context = {'form': form}
            return render(request, 'td/proxy_tracking/proxy_tracking_new.html', context)


def proxy_tracking_edit(request, tid):
    from td.models import ProxyTracking
    from td.forms import ProxyMoveForm
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    tracking = get_object_or_404(ProxyTracking, id=tid)

    if request.method == 'GET':
        form = ProxyMoveForm(instance=tracking)
        context = {'form': form}
        return render(request, 'td/proxy_tracking/proxy_tracking_edit.html', context)

    elif request.method == 'POST':
        rotate_token(request)
        form = ProxyMoveForm(request.POST, instance=tracking)

        if form.is_valid():
            track = form.save(commit=False)
            track.added_by = request.user
            track.save()
            messages.success(request, 'Изменения внесены')
            return redirect(to='td:proxy_info', pid=tracking.proxy.id)
        else:
            context = {'form': form}
            return render(request, 'td/proxy_tracking/proxy_tracking_edit.html', context)


def proxy_tracking_delete(request, tid):
    from td.models import ProxyTracking

    tracking = get_object_or_404(ProxyTracking, id=tid)
    pid = tracking.proxy.id
    tracking.delete()
    messages.success(request, 'Предача удалена')
    return redirect(to='td:proxy_info', pid=pid)