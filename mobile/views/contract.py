from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.middleware.csrf import rotate_token


def contract_new(request):
    from mobile.forms import ContractForm

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        form = ContractForm()
        context = {'form': form}
        return render(request, 'mobile/contract/new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = ContractForm(request.POST)

        if form.is_valid():
            contract = form.save()
            messages.success(request, 'Договор добавлен')
            return redirect(to='mobile:contract_info', uid=contract.id)
        else:
            context = {'form': form}
            return render(request, 'mobile/contract/new.html', context)


def contract_info(request, uid):
    from mobile.models import Contract

    contract = get_object_or_404(Contract, id=uid)
    context = {'contract': contract}
    return render(request, 'mobile/contract/info.html', context)


def contract_edit(request, uid):
    from mobile.models import Contract
    from mobile.forms import ContractForm

    contract = get_object_or_404(Contract, id=uid)
    if request.method == 'GET':
        form = ContractForm(instance=contract)
        context = {'form': form}
        return render(request, 'mobile/contract/edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            contract = form.save()
            messages.success(request, 'Изменения применены')
            return redirect(to='mobile:contract_info', uid=contract.id)
        else:
            context = {'form': form}
            return render(request, 'mobile/contract/edit.html', context)


def contract_list(request, show_all=False):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from mobile.models import Contract

    if show_all:
        contracts = Contract.objects.order_by('name')
    else:
        contracts = Contract.objects.filter(active=True).order_by('name')

    context = {
        'contracts': contracts,
        'show_all': show_all
    }

    return render(request, 'mobile/contract/list.html', context)


def contract_delete(request, uid):
    from mobile.models import Contract

    contract = get_object_or_404(Contract, id=uid)

    if contract.active:
        contract.active = False
        messages.warning(request, 'Договор удален')
    else:
        contract.active = True
        messages.warning(request, 'Договор восстановлен')
    contract.save()
    if request.GET.get('return', '') == 'contract_info':
        return redirect(to='mobile:contract_info', uid=contract.id)
    else:
        return redirect(to='mobile:contract_list')
