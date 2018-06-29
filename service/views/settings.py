from django.shortcuts import HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from main.backends import render_mobile as render


def settings(request):
    from service.forms import GlobalSettingsForm
    from django.forms import modelformset_factory
    from main.models import GlobalSettings

    keys_list = [
        'service_email_footer',
        #'service_email_from',
    ]

    settings_list = GlobalSettings.objects.filter(key__in=keys_list).order_by('name')
    settings_factory = modelformset_factory(GlobalSettings, form=GlobalSettingsForm, extra=len(keys_list))

    if request.method == 'GET':
        formset = settings_factory(queryset=settings_list)

        rows = []

        for i, elem in enumerate(settings_list):
            rows.append({
                'name': elem.name,
                'form': formset[i]
            })

        context = {
            'formset': rows,
            'management_form': formset.management_form
        }

        return render(request, 'service/settings.html', context)
    elif request.method == 'POST':
        formset = settings_factory(request.POST, queryset=settings_list)

        if formset.is_valid():
            formset.save()
            messages.success(request, 'Изменения применены')
            return redirect(to='service:settings')
        else:
            messages.error(request, 'Не удалось применить изменения')
            return redirect(to='service:settings')
    else:
        return HttpResponse('Метод не поддерживается')
