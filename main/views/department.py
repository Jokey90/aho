from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from main.backends import render_mobile as render


def department_list(request):
    from main.models import Department

    if request.GET.get('all', 0):
        deps = Department.objects.all()
    else:
        deps = Department.objects.filter(active=True).all()

    def walk_deps_tree(lst, res=[], root=None, level=0):
        for item in lst:
            if item.parent_department_id == root:
                item.level = range(level)
                res.append(item)
                walk_deps_tree(lst, res, root=item.id, level=level+1)
        return res

    context = {
        'deps': walk_deps_tree(deps)
    }

    return render(request, 'main/department/department_list.html', context)


def department_info(request, did):
    from main.models import Department, Employee

    dep = get_object_or_404(Department, id=did)
    child_deps = Department.objects.filter(parent_department=dep).all()
    emps = Employee.objects.filter(department=dep, active=True).all()

    context = {
        'dep': dep,
        'child_deps': child_deps,
        'emps': emps
    }

    return render(request, 'main/department/department_info.html', context)


def department_new(request):
    from main.forms import DepartmentForm
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        form = DepartmentForm()

        context = {'form': form}
        return render(request, 'main/department/department_new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = DepartmentForm(request.POST)

        if form.is_valid():
            dep = form.save()
            messages.success(request, 'Подразделение добавлено')
            return redirect(to='main:department_info', did=dep.id)
        else:
            context = {'form': form}
            return render(request, 'main/department/department_new.html', context)


def department_edit(request, did):
    from main.forms import DepartmentForm
    from main.models import Department
    from django.middleware.csrf import rotate_token

    if request.method == 'GET':
        dep = get_object_or_404(Department, id=did)
        form = DepartmentForm(instance=dep)
        context = {'form': form}
        return render(request, 'main/department/department_edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        dep = get_object_or_404(Department, id=did)
        form = DepartmentForm(request.POST, instance=dep)

        if form.is_valid():
            form.save()
            messages.success(request, 'Подразделение изменено')
            return redirect(to='main:department_info', did=did)
        else:
            context = {'form': form}
            return render(request, 'main/department/department_edit.html', context)


def department_delete(request, did):
    from main.models import Department

    dep = get_object_or_404(Department, id=did)
    if request.user.is_superuser:
        if dep.active:
            dep.active = False
            messages.success(request, 'Подразделение удалено')
        else:
            dep.active = True
            messages.success(request, 'Подразделение восстановлено')
        dep.save()
    else:
        messages.error(request, 'Недостаточно прав')

    return redirect(to='main:department_list')