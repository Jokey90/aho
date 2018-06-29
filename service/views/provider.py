from django.shortcuts import HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from main.backends import render_mobile as render


def provider_list(request):
    from service.models import Provider

    providers = Provider.objects.order_by('name')
    context = {'providers': providers}
    return render(request, 'service/provider/list.html', context)


def provider_info(request, uid):
    from service.models import Provider

    provider = get_object_or_404(Provider, id=uid)
    context = {'provider': provider}
    return render(request, 'service/provider/info.html', context)


def provider_new(request):
    from service.forms import ProviderEditForm
    from service.models import Provider

    if request.method == 'GET':
        form = ProviderEditForm()
        context = {'form': form}
        return render(request, 'service/provider/new.html', context)
    elif request.method == 'POST':
        form = ProviderEditForm(request.POST)
        if form.is_valid():
            provider = form.save()
            messages.success(request, 'Провайдер добавлен')
            return redirect(to='service:provider_info', uid=provider.id)
        else:
            context = {'form': form}
            return render(request, 'service/provider/new.html', context)


def provider_edit(request, uid):
    from service.models import Provider
    from service.forms import ProviderEditForm

    provider = get_object_or_404(Provider, id=uid)

    if request.method == 'GET':
        form = ProviderEditForm(instance=provider)
        context = {'form': form}
        return render(request, 'service/provider/edit.html', context)
    elif request.method == 'POST':
        form = ProviderEditForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения применены')
            return redirect(to='service:provider_info', uid=uid)
        else:
            context = {'form': form}
            return render(request, 'service/provider/edit.html', context)
