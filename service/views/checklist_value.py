from django.shortcuts import HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from main.backends import render_mobile as render


def checklist_value_info(request, uid):
    from service.models import ChecklistValue

    value = get_object_or_404(ChecklistValue, id=uid)

    context = {
        'value': value
    }
    return render(request, 'service/checklist_value/info.html', context)


def checklist_value_solve(request, uid):
    from service.models import ChecklistValue, Ticket
    from service.forms import ChecklistValueSolveForm
    from datetime import datetime

    value = get_object_or_404(ChecklistValue, id=uid)
    return_path = request.GET.get('return', 'checklist_value_info')
    ticket = next(iter(Ticket.objects.filter(issue_id=uid)), None)

    if not value.has_issues or value.solve_date is not None:
        messages.debug(request, 'Ничего не произошло')
        return redirect(to='service:checklist_value_info', uid=value.id)

    form = ChecklistValueSolveForm(instance=value, initial={'solve_date': datetime.now()})

    if request.method == 'POST':
        form = ChecklistValueSolveForm(request.POST, instance=value)
        if form.is_valid():
            value = form.save()
            messages.success(request, 'Замечание устранено')
            if form.cleaned_data['close_ticket'] and ticket is not None:
                if ticket.close_date is None:
                    ticket.close_date = value.solve_date
                    ticket.save()
                    messages.success(request, 'Заявка закрыта')

            if return_path == 'checklist_info':
                return redirect(to='service:checklist_info', uid=value.checklist_id)
            elif return_path == 'checklist_value_list':
                return redirect(to='service:checklist_value_list', state='unsolved')
            else:
                return redirect(to='service:checklist_value_info', uid=value.id)

    if ticket is None or ticket.close_date is not None:
        form.fields.pop('close_ticket')
    context = {
        'value': value,
        'form': form
    }
    return render(request, 'service/checklist_value/close.html', context)


def checklist_value_edit(request, uid):
    from service.models import ChecklistValue
    from service.forms import ChecklistValueEditForm

    value = get_object_or_404(ChecklistValue, id=uid)

    if request.method == 'GET':
        form = ChecklistValueEditForm(instance=value)
        context = {
            'value': value,
            'form': form
        }
        return render(request, 'service/checklist_value/edit.html', context)
    elif request.method == 'POST':
        form = ChecklistValueEditForm(request.POST, request.FILES, instance=value)

        if form.is_valid():
            value = form.save()
            if value.solve_date is not None:
                value.has_issues = True
            value.save()
            messages.success(request, 'Изменения применены')
            return redirect(to='service:checklist_value_info', uid=value.id)
        else:
            context = {
                'value': value,
                'form': form
            }
            return render(request, 'service/checklist_value/edit.html', context)


def checklist_value_list(request, state='all'):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from service.models import ChecklistValue

    page = request.GET.get('page', 1)

    if state == 'all':
        data = ChecklistValue.objects.filter(has_issues=True).order_by('-checklist__date')
        title = 'Замечания'
    elif state == 'solved':
        data = ChecklistValue.objects.filter(has_issues=True, solve_date__isnull=False).order_by('-checklist__date')
        title = 'Устраненные замечания'
    else:
        data = ChecklistValue.objects.filter(has_issues=True, solve_date__isnull=True).order_by('-checklist__date')
        title = 'Неустраненные замечания'

    paginator = Paginator(data, 25)

    try:
        checklist_values = paginator.page(page)
    except PageNotAnInteger:
        checklist_values = paginator.page(1)
    except EmptyPage:
        checklist_values = paginator.page(paginator.num_pages)

    context = {
        'checklist_values': checklist_values,
        'title': title
    }
    return render(request, 'service/checklist_value/list.html', context)
