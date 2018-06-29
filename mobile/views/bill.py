from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.middleware.csrf import rotate_token


def bill_file_upload(request):
    from mobile.forms import BillFileForm

    if request.method == 'GET':
        form = BillFileForm()
        context = {'form': form}
        return render(request, 'mobile/bill/upload.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = BillFileForm(request.POST, request.FILES)

        for _ in range(1):

            if form.is_valid() and len(request.FILES) == 1:
                filetype = form.cleaned_data['file'].name.split('.')[-1]
                if filetype in ['xls', 'xlsx']:
                    import xlrd, re
                    from datetime import date
                    from mobile.models import Bill, Contract, Sim

                    active_contracts = Contract.objects.filter(active=True)

                    num_test = re.compile('[0-9]{8,10}')

                    bill_file = form.save()
                    wb = xlrd.open_workbook(bill_file.file.path, formatting_info=False)
                    ws = wb.sheet_by_index(0)

                    if ws.cell_value(0, 0) == 'Номер телефона':   # проверка на билайн
                        number_col = 0
                        contract_col = None
                        group_col = None
                        amount_col = None

                        for col in range(0, ws.ncols):
                            cell_value = ws.cell_value(rowx=0, colx=col)
                            if cell_value == 'Договор':
                                contract_col = col
                                continue
                            if cell_value == 'Группа счетов':
                                group_col = col
                                continue
                            if cell_value == 'Перенесенные начисления по абон. плате и звонкам':
                                amount_col = col
                                continue

                        if contract_col is None or group_col is None or amount_col is None:
                            messages.error(request, 'Неверный файл')
                            break

                        for row in range(1, ws.nrows):
                            sim_num = str(ws.cell_value(rowx=row, colx=number_col)).replace('.0', '')
                            contract_num = str(ws.cell_value(rowx=row, colx=contract_col)).replace('.0', '')
                            group_num = str(ws.cell_value(rowx=row, colx=group_col)).replace('.0', '')
                            if num_test.match(sim_num):
                                if active_contracts.filter(number=contract_num, group=group_num).exists():
                                    bill = Bill(number=sim_num)
                                    bill.contract = active_contracts.get(number=contract_num, group=group_num)
                                    bill.amount = ws.cell_value(rowx=row, colx=amount_col) * 1.18
                                    bill.period = date(bill_file.year, bill_file.month, 1)
                                    bill.bill_file = bill_file
                                    if Sim.objects.filter(number=sim_num).exists():
                                        bill.sim = Sim.objects.get(number=sim_num)
                                    bill.save()
                                else:
                                    continue
                    elif ws.cell_value(0, 0) == 'Номер':  # МТС
                        number_col = 0
                        amount_col = None

                        for col in range(0, ws.ncols):
                            cell_value = ws.cell_value(rowx=0, colx=col)
                            if cell_value == 'Израсходовано за период':
                                amount_col = col
                                break

                        if amount_col is None:
                            messages.error(request, 'Неверный файл')
                            break

                        contract_mts = Contract.objects.filter(mts=True, active=True).first()

                        for row in range(1, ws.nrows):
                            sim_num = str(ws.cell_value(rowx=row, colx=number_col))[1:]
                            if num_test.match(sim_num):
                                bill = Bill(number=sim_num)
                                bill.contract = contract_mts
                                bill.amount = ws.cell_value(rowx=row, colx=amount_col)
                                bill.period = date(bill_file.year, bill_file.month, 1)
                                bill.bill_file = bill_file
                                if Sim.objects.filter(number=sim_num).exists():
                                    bill.sim = Sim.objects.get(number=sim_num)
                                bill.save()
                            else:
                                continue

                    messages.success(request, 'Счет загружен')
                    return redirect(to='mobile:bill_file_info', uid=bill_file.id)
                else:
                    messages.error(request, 'Неверный формат файла')
                    break
            else:
                break

        context = {'form': form}
        return render(request, 'mobile/bill/upload.html', context)


def bill_file_list(request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from mobile.models import BillFile

    page = request.GET.get('page', 1)

    data = BillFile.objects.order_by('-year', '-month')

    paginator = Paginator(data, 20)

    try:
        bills = paginator.page(page)
    except PageNotAnInteger:
        bills = paginator.page(1)
    except EmptyPage:
        bills = paginator.page(paginator.num_pages)

    context = {
        'bills': bills
    }

    return render(request, 'mobile/bill/file_list.html', context)


def bill_file_info(request, uid):
    from mobile.models import BillFile

    bill_file = get_object_or_404(BillFile, id=uid)

    context = {'bill_file': bill_file}
    return render(request, 'mobile/bill/file_info.html', context)


def bill_file_edit(request, uid):
    from mobile.models import BillFile, Bill
    from mobile.forms import BillFileEditForm
    from datetime import date

    bill_file = get_object_or_404(BillFile, id=uid)
    if request.method == 'GET':
        form = BillFileEditForm(instance=bill_file)
        context = {'form': form}
        return render(request, 'mobile/bill/file_edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = BillFileEditForm(request.POST, instance=bill_file)
        if form.is_valid():
            bill_file = form.save()
            for bill in bill_file.bill_set.all():
                if bill.contract.mts:
                    bill.period = date(bill_file.year, bill_file.month, 1)
                    bill.save()
            messages.success(request, 'Изменения применены')
            return redirect(to='mobile:bill_file_info', uid=bill_file.id)
        else:
            context = {'form': form}
            return render(request, 'mobile/bill/file_edit.html', context)


def bill_file_delete(request, uid):
    from mobile.models import BillFile, Bill

    bill_file = get_object_or_404(BillFile, id=uid)
    for bill in bill_file.bill_set.all():
        bill.delete()
    bill_file.file.delete()
    bill_file.delete()
    messages.warning(request, 'Счет и все связанные расходы удалены')
    return redirect(to='mobile:bill_file_list')


def bill_file_refresh(request, uid):
    from mobile.models import BillFile, Sim

    bill_file = get_object_or_404(BillFile, id=uid)
    sims = Sim.objects.all()

    for bill in bill_file.bill_set.all():
        if sims.filter(number=bill.number).exists():
            bill.sim = sims.get(number=bill.number)
            bill.save()

    return redirect(to='mobile:bill_file_list')


def bill_file_link_all(request, uid):
    from mobile.models import BillFile, Sim

    bill_file = get_object_or_404(BillFile, id=uid)
    sims = Sim.objects.all()

    for bill in bill_file.bill_set.filter(sim=None).all():
        if not sims.filter(number=bill.number).exists():
            sim = Sim(number=bill.number)
            sim.save()
            bill.sim = sim
            bill.save()
        else:
            sim = sims.get(number=bill.number)
            bill.sim = sim
            bill.save()

    return redirect(to='mobile:bill_file_list')
