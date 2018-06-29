from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib import messages


def accident_doc_new(request):
    from django.middleware.csrf import rotate_token
    from td.forms import AccidentDocForm
    from td.models import AccidentDoc

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        accident = request.GET.get('accident', None)
        form = AccidentDocForm(initial={'accident': accident})
        context = {'form': form}
        return render(request, 'td/accident_doc/accident_doc_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = AccidentDocForm(request.POST, request.FILES)

        if form.is_valid():
            accident_doc = form.save()
            messages.success(request, 'Объект добавлен')
            return redirect(to='td:accident_info', aid=accident_doc.accident.id)
        else:
            context = {'form': form}
            return render(request, 'td/accident_doc/accident_doc_new.html', context)


def accident_doc_info(request, did):
    from td.models import AccidentDoc

    doc = get_object_or_404(AccidentDoc, id=did)

    context = {
        'doc': doc
    }

    return render(request, 'td/accident_doc/accident_doc_info.html', context)


def accident_doc_edit(request, did):
    from td.models import AccidentDoc
    from td.forms import AccidentDocForm
    from django.middleware.csrf import rotate_token

    return_path = request.GET.get('return', None)
    doc = get_object_or_404(AccidentDoc, id=did)

    if request.method == 'GET':
        form = AccidentDocForm(instance=doc)
        context = {'form': form}
        return render(request, 'td/accident_doc/accident_doc_edit.html', context)

    elif request.method == 'POST':
        rotate_token(request)
        form = AccidentDocForm(request.POST, request.FILES, instance=doc)

        if form.is_valid():
            form.save()
            messages.success(request, 'Объект изменен')
            return redirect(to='td:accident_info', aid=doc.accident.id)
        else:
            context = {'form': form}
            return render(request, 'td/accident_doc/accident_doc_edit.html', context)


def accident_doc_delete(request, did):
    from td.models import AccidentDoc

    return_path = request.GET.get('return', None)
    doc = get_object_or_404(AccidentDoc, id=did)
    doc.scan.delete()
    doc.delete()
    return redirect(to='td:accident_info', aid=doc.accident.id)