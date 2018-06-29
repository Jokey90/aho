from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib import messages


def accident_new(request):
    from django.middleware.csrf import rotate_token
    from td.forms import AccidentForm
    from td.models import Accident

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        car = request.GET.get('car', None)
        form = AccidentForm(initial={'car': car}, new=True)
        context = {'form': form}
        return render(request, 'td/accident/accident_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = AccidentForm(request.POST, request.FILES, new=True)

        if form.is_valid():
            accident = form.save()
            messages.success(request, 'Объект добавлен')
            if return_path == 'car_accidents':
                return redirect(to='td:car_accidents', cid=accident.car.id)
            else:
                return redirect(to='td:accident_info', aid=accident.id)
        else:
            context = {'form': form}
            return render(request, 'td/accident/accident_new.html', context)


def accident_info(request, aid):
    from td.models import Accident, AccidentDoc

    accident = get_object_or_404(Accident, id=aid)
    docs = AccidentDoc.objects.filter(accident=accident).all()

    context = {
        'accident': accident,
        'docs': docs
    }

    return render(request, 'td/accident/accident_info.html', context)


def accident_edit(request, aid):
    from td.models import Accident
    from td.forms import AccidentForm
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    accident = get_object_or_404(Accident, id=aid)

    if request.method == 'GET':
        form = AccidentForm(instance=accident)
        context = {'form': form}
        return render(request, 'td/accident/accident_edit.html', context)

    elif request.method == 'POST':
        rotate_token(request)
        form = AccidentForm(request.POST, request.FILES, instance=accident)

        if form.is_valid():
            form.save()
            messages.success(request, 'Объект изменен')
            if return_path == 'car_accidents':
                return redirect(to='td:car_accidents', cid=accident.car.id)
            else:
                return redirect(to='td:accident_info', aid=aid)
        else:
            context = {'form': form}
            return render(request, 'td/accident/accident_edit.html', context)


def accident_delete(request, aid):
    from td.models import Accident, AccidentDoc

    return_path = request.GET.get('return', None)
    accident = get_object_or_404(Accident, id=aid)
    for doc in AccidentDoc.objects.filter(accident=accident).all():
        doc.scan.delete()
        doc.delete()

    accident.delete()
    return redirect(to='td:car_accidents', cid=accident.car.id)