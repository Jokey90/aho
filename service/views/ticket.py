from django.shortcuts import HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from main.backends import render_mobile as render


def send_mail(ticket, attach_file=False):
    from main.models import GlobalSettings
    from django.core.mail import EmailMultiAlternatives
    from main import settings

    subject = ticket.subject
    from_email = settings.EMAIL_SENDER_FROM
    recipient_list = [ticket.provider.contact.email]
    footer_text = GlobalSettings.objects.get_setting('service_email_footer').value
    html_message = ticket.text.replace('\n', '<br/>') + '<br/><br/>' + footer_text.replace('\n', '<br/>')
    text_message = ticket.text + '\n\n' + footer_text

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=from_email,
        to=recipient_list
    )
    email.attach_alternative(html_message, 'text/html')

    if attach_file:
        if ticket.issue and ticket.issue.photo:
            email.attach_file(ticket.issue.photo.path)

    if ticket.photo:
        email.attach_file(ticket.photo.path)

    email_sent = False
    error = ''
    try:
        email_sent = email.send()
    except Exception as e:
        error = str(e)

    return {'sent': email_sent, 'error': error}


def ticket_new(request):
    from service.forms import TicketNewForm
    from main.models import GlobalSettings
    from django.core.mail import EmailMultiAlternatives

    if request.method == 'GET':
        issue_id = request.GET.get('issue_id', None)
        form = TicketNewForm(initial={'issue': issue_id})
        context = {'form': form}
        return render(request, 'service/ticket/new.html', context)
    elif request.method == 'POST':
        form = TicketNewForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['issue'] is not None and form.cleaned_data['issue'].has_ticket():
                messages.error(request, 'К выбранному замечанию уже создана заявка')
            else:
                ticket = form.save()

                email = send_mail(ticket, form.cleaned_data['attach_file'])

                if email['sent']:
                    messages.success(request, 'Заявка создана')
                    messages.success(request, 'Письмо отправлено')
                    ticket.mail_sent = True
                    ticket.save()
                    return redirect(to='service:ticket_info', uid=ticket.id)
                else:
                    messages.warning(request, 'Заявка создана')
                    messages.error(request, 'Письмо НЕ отправлено')
                    messages.debug(request, email['error'])
                    return redirect(to='service:ticket_info', uid=ticket.id)

        context = {'form': form}
        return render(request, 'service/ticket/new.html', context)


def ticket_resend_email(request, uid):
    from service.models import Ticket
    from main.models import GlobalSettings
    from django.core.mail import EmailMultiAlternatives

    ticket = get_object_or_404(Ticket, id=uid)

    email = send_mail(ticket, True)

    if email['sent']:
        messages.success(request, 'Письмо отправлено')
        ticket.mail_sent = True
        ticket.save()
        return redirect(to='service:ticket_info', uid=ticket.id)
    else:
        messages.error(request, 'Письмо не отправлено')
        messages.debug(request, email['error'])
        return redirect(to='service:ticket_info', uid=ticket.id)


def ticket_info(request, uid):
    from service.models import Ticket

    ticket = get_object_or_404(Ticket, id=uid)

    context = {
        'ticket': ticket
    }
    return render(request, 'service/ticket/info.html', context)


def ticket_list(request, state='all'):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from service.models import Ticket

    page = request.GET.get('page', 1)
    title = 'Завки'

    if state == 'active':
        data = Ticket.objects.filter(close_date__isnull=True).order_by('-creation_datetime')
        title = 'Заявки в работе'
    elif state == 'closed':
        data = Ticket.objects.filter(close_date__isnull=False).order_by('-creation_datetime')
        title = 'Закрытые заявки'
    else:
        data = Ticket.objects.order_by('-creation_datetime')

    paginator = Paginator(data, 25)

    try:
        tickets = paginator.page(page)
    except PageNotAnInteger:
        tickets = paginator.page(1)
    except EmptyPage:
        tickets = paginator.page(paginator.num_pages)

    context = {
        'tickets': tickets,
        'title': title
    }
    return render(request, 'service/ticket/list.html', context)


def ticket_edit(request, uid):
    from service.forms import TicketEditForm
    from service.models import Ticket, ChecklistValue

    ticket = get_object_or_404(Ticket, id=uid)

    if request.method == 'GET':
        form = TicketEditForm(instance=ticket)
        form.fields['issue'].queryset |= ChecklistValue.objects.filter(id=ticket.issue_id)
        context = {'form': form}
        return render(request, 'service/ticket/edit.html', context)
    elif request.method == 'POST':
        form = TicketEditForm(request.POST, request.FILES, instance=ticket)
        form.fields['issue'].queryset |= ChecklistValue.objects.filter(id=ticket.issue_id)

        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения применены')
            return redirect(to='service:ticket_info', uid=ticket.id)
        else:
            context = {'form': form}
            return render(request, 'service/ticket/edit.html', context)


def ticket_close(request, uid):
    from service.models import Ticket, ChecklistValue
    from service.forms import TicketColseForm
    from datetime import datetime

    ticket = get_object_or_404(Ticket, id=uid)
    return_path = request.GET.get('return', 'ticket_info')

    if ticket.close_date is not None:
        messages.warning(request, 'Невозможно изменить статус заявки')
        return redirect(to='service:ticket_info', uid=ticket.id)

    form = TicketColseForm(instance=ticket, initial={'close_date': datetime.now()})

    if request.method == 'POST':
        form = TicketColseForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            messages.success(request, 'Заявка закрыта')
            if form.cleaned_data['solve_issue']:
                issue = ChecklistValue.objects.get(id=ticket.issue_id)
                issue.solve_date = ticket.close_date
                issue.save()
                messages.success(request, 'Замечание устранено')
            if return_path == 'ticket_list':
                return redirect(to='service:ticket_list', state='active')
            else:
                return redirect(to='service:ticket_info', uid=uid)

    if ticket.issue is None or ticket.issue.solve_date is not None:
        form.fields.pop('solve_issue')
    context = {
        'ticket': ticket,
        'form': form
    }
    return render(request, 'service/ticket/close.html', context)
