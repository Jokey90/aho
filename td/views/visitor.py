from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages


def visitor_list(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from td.models import VisitorsParking

    page = request.GET.get('page', 1)
    data = VisitorsParking.objects.order_by('-date', '-time').all()

    paginator = Paginator(data, 20)

    try:
        visitors = paginator.page(page)
    except PageNotAnInteger:
        visitors = paginator.page(1)
    except EmptyPage:
        visitors = paginator.page(paginator.num_pages)

    context = {
        'visitors': visitors
    }

    return render(request, 'td/visitor/visitor_list.html', context)


def visitor_info(request, vid):
    from td.models import VisitorsParking

    visitor = get_object_or_404(VisitorsParking, id=vid)

    context = {
        'visitor': visitor
    }

    return render(request, 'td/visitor/visitor_info.html', context)


def visitor_new(request):
    from td.forms import VisitorsParkingForm
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        form = VisitorsParkingForm(new=True)

        context = {'form': form}
        return render(request, 'td/visitor/visitor_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = VisitorsParkingForm(request.POST, new=True)

        if form.is_valid():
            visitor = form.save()
            messages.success(request, 'Гость добавлен')
            return redirect(to='td:visitor_info', vid=visitor.id)
        else:
            context = {'form': form}
            return render(request, 'td/visitor/visitor_new.html', context)


def visitor_edit(request, vid):
    from td.forms import VisitorsParkingForm
    from td.models import VisitorsParking
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        visitor = get_object_or_404(VisitorsParking, id=vid)
        form = VisitorsParkingForm(instance=visitor)
        context = {'form': form}
        return render(request, 'td/visitor/visitor_edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        visitor = get_object_or_404(VisitorsParking, id=vid)
        form = VisitorsParkingForm(request.POST, instance=visitor)

        if form.is_valid():
            form.save()
            messages.success(request, 'Запись изменена')
            return redirect(to='td:visitor_info', vid=vid)
        else:
            context = {'form': form}
            return render(request, 'td/visitor/visitor_edit.html', context)


def visitor_delete(request, vid):
    from td.models import VisitorsParking

    item = get_object_or_404(VisitorsParking, id=vid)
    item.delete()
    messages.success(request, 'Запись удалена')

    return redirect(to='td:visitor_list')