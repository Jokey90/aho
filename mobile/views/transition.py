from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.middleware.csrf import rotate_token


def transition_list(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from mobile.models import Transition

    page = request.GET.get('page', 1)
    data = Transition.objects.order_by('-date')

    paginator = Paginator(data, 20)

    try:
        transitions = paginator.page(page)
    except PageNotAnInteger:
        transitions = paginator.page(1)
    except EmptyPage:
        transitions = paginator.page(paginator.num_pages)

    context = {
        'transitions': transitions
    }

    return render(request, 'mobile/transition/list.html', context)


def transition_new(request, uid=None):
    from django.middleware.csrf import rotate_token
    from mobile.forms import TransitionForm
    from datetime import datetime

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        form = TransitionForm(initial={'sim': uid, 'date_field': datetime.now()})
        context = {'form': form}
        return render(request, 'mobile/transition/new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = TransitionForm(request.POST)

        if form.is_valid():
            transition = form.save(commit=False)
            transition.date = form.cleaned_data['date_field']
            transition.save()
            messages.success(request, 'SIM-карта передана')
            return redirect(to='mobile:sim_info', uid=transition.sim.id)
        else:
            context = {'form': form}
            return render(request, 'mobile/transition/new.html', context)


def transition_edit(request, uid):
    from mobile.models import Transition
    from mobile.forms import TransitionForm

    transition = get_object_or_404(Transition, id=uid)
    if request.method == 'GET':
        form = TransitionForm(instance=transition, initial={'date_field': transition.date})
        context = {'form': form}
        return render(request, 'mobile/transition/edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = TransitionForm(request.POST, instance=transition)
        if form.is_valid():
            transition = form.save(commit=False)
            transition.date = form.cleaned_data['date_field']
            transition.save()
            messages.success(request, 'Изменения применены')
            return redirect(to='mobile:sim_transitions', uid=transition.sim.id)
        else:
            context = {'form': form}
            return render(request, 'mobile/transition/edit.html', context)


def transition_delete(request, uid):
    from mobile.models import Transition

    transition = get_object_or_404(Transition, id=uid)

    sim_id = transition.sim_id

    transition.delete()
    messages.warning(request, 'Запись удалена')

    return redirect(to='mobile:sim_transitions', uid=sim_id)
