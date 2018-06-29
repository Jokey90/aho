from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from main.backends import render_mobile as render


def contact_list(request):
    from main.models import Contact

    contacts = Contact.objects.order_by('name')

    context = {
        'contacts': contacts
    }

    return render(request, 'main/contact/list.html', context)


def contact_info(request, uid):
    from main.models import Contact

    contact = get_object_or_404(Contact, id=uid)

    context = {
        'contact': contact
    }

    return render(request, 'main/contact/info.html', context)


def contact_edit(request, uid):
    from main.models import Contact
    from main.forms import ContactEditForm

    contact = get_object_or_404(Contact, id=uid)
    form = ContactEditForm(instance=contact)

    if request.method == 'POST':
        form = ContactEditForm(request.POST, instance=contact)

        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения применены')
            return redirect(to='main:contact_info', uid=uid)
        else:
            messages.error(request, 'Ошибка заполнения формы')

    context = {
        'form': form
    }

    return render(request, 'main/contact/edit.html', context)


def contact_new(request):
    from main.models import Contact
    from main.forms import ContactEditForm

    form = ContactEditForm()

    if request.method == 'POST':
        form = ContactEditForm(request.POST)

        if form.is_valid():
            contact = form.save()
            messages.success(request, 'Контакт создан')
            return redirect(to='main:contact_info', uid=contact.id)
        else:
            messages.error(request, 'Ошибка заполнения формы')

    context = {
        'form': form
    }
    return render(request, 'main/contact/new.html', context)
