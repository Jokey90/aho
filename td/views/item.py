from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib import messages


def item_list(request):   #wrecked
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from td.models import Key

    keys_list = Key.objects.order_by('type', 'car__name', 'car__number').all()

    paginator = Paginator(keys_list, 10)
    page = request.GET.get('page')

    try:
        keys = paginator.page(page)
    except PageNotAnInteger:
        keys = paginator.page(1)
    except EmptyPage:
        keys = paginator.page(paginator.num_pages)

    context = {
        'keys': keys
    }

    return render(request, 'td/key/key_list.html', context)


def item_new(request, item_type):
    from django.middleware.csrf import rotate_token
    from td.forms import DocForm, EnsuranceForm, KeyForm
    from td.models import Item

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        car = request.GET.get('car', None)
        if item_type == 'doc':
            form = DocForm(initial={'car': car}, new=True)
        elif item_type == 'ensurance':
            form = EnsuranceForm(initial={'car': car}, new=True)
        elif item_type == 'key':
            form = KeyForm(initial={'car': car}, new=True)
        else:
            return HttpResponseNotFound()

        form.fields['type'].choices = [(x[1], x[2]) for x in Item.TYPES if x[0] == item_type]
        context = {'form': form}
        return render(request, 'td/item/item_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        if item_type == 'doc':
            form = DocForm(request.POST, request.FILES, new=True)
        elif item_type == 'ensurance':
            form = EnsuranceForm(request.POST, request.FILES, new=True)
        elif item_type == 'key':
            form = KeyForm(request.POST, request.FILES, new=True)
        else:
            return HttpResponseNotFound()

        if form.is_valid():
            item = form.save()
            messages.success(request, 'Объект добавлен')
            if return_path == 'car_docs':
                return redirect(to='td:car_docs', cid=item.car.id)
            elif return_path == 'car_ensurance':
                return redirect(to='td:car_ensurance', cid=item.car.id)
            elif return_path == 'car_keys':
                return redirect(to='td:car_keys', cid=item.car.id)
            else:
                return redirect(to='td:item_info', iid=item.id)
        else:
            form.fields['type'].choices = [(x[1], x[2]) for x in Item.TYPES if x[0] == item_type]
            context = {'form': form}
            return render(request, 'td/item/item_new.html', context)


def item_info(request, iid):
    from td.models import Item, ItemTracking

    item = get_object_or_404(Item, id=iid)
    tracking = ItemTracking.objects.filter(item=item).order_by('-date')

    context = {
        'item': item,
        'tracking': tracking
    }

    return render(request, 'td/item/item_info.html', context)


def item_edit(request, iid):
    from td.models import Item
    from td.forms import DocForm, KeyForm, EnsuranceForm
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    item = get_object_or_404(Item, id=iid)

    if request.method == 'GET':
        if item.get_type() == 'doc':
            form = DocForm(instance=item)
        elif item.get_type() == 'ensurance':
            form = EnsuranceForm(instance=item)
        elif item.get_type() == 'key':
            form = KeyForm(instance=item)
        else:
            return HttpResponseNotFound()
        context = {'form': form}
        return render(request, 'td/item/item_edit.html', context)

    elif request.method == 'POST':
        rotate_token(request)
        if item.get_type() == 'doc':
            form = DocForm(request.POST, request.FILES, instance=item)
        elif item.get_type() == 'ensurance':
            form = EnsuranceForm(request.POST, request.FILES, instance=item)
        elif item.get_type() == 'key':
            form = KeyForm(request.POST, request.FILES, instance=item)
        else:
            return HttpResponseNotFound()

        if form.is_valid():
            form.save()
            messages.success(request, 'Объект изменен')
            if return_path == 'car_docs':
                return redirect(to='td:car_docs', cid=item.car.id)
            elif return_path == 'car_ensurance':
                return redirect(to='td:car_ensurance', cid=item.car.id)
            elif return_path == 'car_keys':
                return redirect(to='td:car_keys', cid=item.car.id)
            else:
                return redirect(to='td:item_info', iid=iid)
        else:
            context = {'form': form}
            return render(request, 'td/item/item_edit.html', context)


def item_delete(request, iid):
    from td.models import Item

    return_path = request.GET.get('return', None)
    item = get_object_or_404(Item, id=iid)
    if item.active:
        item.active = False
        messages.success(request, 'Объект удачен')
    else:
        item.active = True
        messages.success(request, 'Объект восстановлен')
    item.save()

    if return_path == 'car_docs':
        return redirect(to='td:car_docs', cid=item.car.id)
    elif return_path == 'car_ensurance':
        return redirect(to='td:car_ensurance', cid=item.car.id)
    elif return_path == 'car_keys':
        return redirect(to='td:car_keys', cid=item.car.id)
    else:
        return redirect(to='td:car_list')