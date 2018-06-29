from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib import messages


def item_tracking_new(request, iid):
    from td.models import Item
    from td.forms import ItemMoveForm
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    item = get_object_or_404(Item, id=iid)

    if request.method == 'GET':
        form = ItemMoveForm(initial={'item': item}, new=True)
        context = {'form': form}
        return render(request, 'td/item_tracking/item_tracking_new.html', context)

    elif request.method == 'POST':
        rotate_token(request)
        form = ItemMoveForm(request.POST, new=True)

        if form.is_valid():
            track = form.save(commit=False)
            track.added_by = request.user
            track.save()
            messages.success(request, 'Объект передан')
            if return_path == 'car_docs':
                return redirect(to='td:car_docs', cid=track.item.car.id)
            elif return_path == 'car_ensurance':
                return redirect(to='td:car_ensurance', cid=track.item.car.id)
            elif return_path == 'car_keys':
                return redirect(to='td:car_keys', cid=track.item.car.id)
            else:
                return redirect(to='td:item_info', iid=track.item.id)
        else:
            context = {'form': form}
            return render(request, 'td/item_tracking/item_tracking_new.html', context)


def item_tracking_edit(request, tid):
    from td.models import ItemTracking
    from td.forms import ItemMoveForm
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    tracking = get_object_or_404(ItemTracking, id=tid)

    if request.method == 'GET':
        form = ItemMoveForm(instance=tracking)
        context = {'form': form}
        return render(request, 'td/item_tracking/item_tracking_edit.html', context)

    elif request.method == 'POST':
        rotate_token(request)
        form = ItemMoveForm(request.POST, instance=tracking)

        if form.is_valid():
            track = form.save(commit=False)
            track.added_by = request.user
            track.save()
            messages.success(request, 'Изменения внесены')
            return redirect(to='td:item_info', iid=tracking.item.id)
        else:
            context = {'form': form}
            return render(request, 'td/item_tracking/item_tracking_edit.html', context)


def item_tracking_delete(request, tid):
    from td.models import ItemTracking

    tracking = get_object_or_404(ItemTracking, id=tid)
    iid = tracking.item.id
    tracking.delete()
    messages.success(request, 'Предача удалена')
    return redirect(to='td:item_info', iid=iid)