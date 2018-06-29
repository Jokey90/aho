from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.template import RequestContext
from django.contrib import messages


def to_list(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from td.models import TO

    page = request.GET.get('page', 1)
    data = TO.objects.order_by('-date').all()

    paginator = Paginator(data, 25)

    try:
        tos = paginator.page(page)
    except PageNotAnInteger:
        tos = paginator.page(1)
    except EmptyPage:
        tos = paginator.page(paginator.num_pages)

    context = {
        'tos': tos
    }

    return render(request, 'td/to/to_list.html', context)


def to_new(request):
    from td.forms import TOForm
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        car_id = request.GET.get('car', None)
        form = TOForm(initial={'car': car_id}, new=True)

        context = {'form': form}
        return render(request, 'td/to/to_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = TOForm(request.POST, new=True)

        if form.is_valid():
            to = form.save()
            messages.success(request, 'ТО добавлено')
            if return_path == 'car_to':
                return redirect(to='td:car_to', cid=to.car.id)
            else:
                return redirect(to='td:to_info', tid=to.id)
        else:
            context = {'form': form}
            return render(request, 'td/to/to_new.html', context)


def to_info(request, tid):
    from td.models import TO

    to = get_object_or_404(TO, id=tid)

    context = {
        'to': to
    }

    return render(request, 'td/to/to_info.html', context)


def to_edit(request, tid):
    from td.models import TO
    from td.forms import TOForm
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        to = get_object_or_404(TO, id=tid)
        form = TOForm(instance=to)
        context = {'form': form}
        return render(request, 'td/to/to_edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        to = get_object_or_404(TO, id=tid)
        form = TOForm(request.POST, instance=to)

        if form.is_valid():
            form.save()
            messages.success(request, 'ТО изменено')
            if return_path == 'car_to':
                return redirect(to='td:car_to', cid=to.car.id)
            else:
                return redirect(to='td:to_info', tid=tid)
        else:
            context = {'form': form}
            return render(request, 'td/to/to_edit.html', context)


def to_delete(request, tid):
    from td.models import TO

    return_path = request.GET.get('return', None)
    to = get_object_or_404(TO, id=tid)
    to.delete()
    messages.success(request, 'ТО удалено')

    if return_path == 'car_to':
        return redirect(to='td:car_to', cid=to.car.id)
    else:
        return redirect(to='td:to_list')
