from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from main.backends import render_mobile as render


def employee_list(request):
    from main.models import Employee

    if request.GET.get('all', 0):
        emps = Employee.objects.all().prefetch_related('department')
    else:
        emps = Employee.objects.filter(active=True).all().prefetch_related('department')

    context = {
        'emps': emps
    }

    return render(request, 'main/employee/employee_list.html', context)


def employee_info(request, eid):
    from main.models import Employee

    emp = get_object_or_404(Employee, id=eid)

    context = {
        'emp': emp
    }

    return render(request, 'main/employee/employee_info.html', context)


def employee_new(request):
    from main.forms import EmployeeForm
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        form = EmployeeForm()

        context = {'form': form}
        return render(request, 'main/employee/employee_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = EmployeeForm(request.POST)

        if form.is_valid():
            emp = form.save()
            messages.success(request, 'Сотрудник добавлен')
            return redirect(to='main:employee_info', eid=emp.id)
        else:
            context = {'form': form}
            return render(request, 'main/employee/employee_new.html', context)


def employee_edit(request, eid):
    from main.forms import EmployeeForm
    from main.models import Employee
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        emp = get_object_or_404(Employee, id=eid)
        form = EmployeeForm(instance=emp)
        context = {'form': form}
        return render(request, 'main/employee/employee_edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        emp = get_object_or_404(Employee, id=eid)
        form = EmployeeForm(request.POST, instance=emp)

        if form.is_valid():
            form.save()
            messages.success(request, 'Сотрудник изменен')
            return redirect(to='main:employee_info', eid=eid)
        else:
            context = {'form': form}
            return render(request, 'main/employee/employee_edit.html', context)


def employee_delete(request, eid):
    from main.models import Employee

    emp = get_object_or_404(Employee, id=eid)
    if request.user.is_superuser:
        if emp.active:
            emp.active = False
            messages.success(request, 'Сотрудник удален')
        else:
            emp.active = True
            messages.success(request, 'Сотрудник восстановлен')
        emp.save()
    else:
        messages.error(request, 'Недостаточно прав')

    return redirect(to='main:employee_list')