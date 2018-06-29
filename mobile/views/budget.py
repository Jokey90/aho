from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.middleware.csrf import rotate_token


def budget_new(request):
    from mobile.forms import BudgetForm

    return_path = request.GET.get('return', None)
    if request.method == 'GET':
        form = BudgetForm()
        context = {'form': form}
        return render(request, 'mobile/budget/new.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = BudgetForm(request.POST)

        if form.is_valid():
            budget = form.save()
            messages.success(request, 'Бюджет добавлен')
            return redirect(to='mobile:budget_list')
        else:
            context = {'form': form}
            return render(request, 'mobile/budget/new.html', context)


def budget_list(request):
    from mobile.models import Budget

    budgets = Budget.objects.order_by('-year', 'division')

    context = {
        'budgets': budgets
    }

    return render(request, 'mobile/budget/list.html', context)


def budget_edit(request, uid):
    from mobile.models import Budget
    from mobile.forms import BudgetForm

    budget = get_object_or_404(Budget, id=uid)
    if request.method == 'GET':
        form = BudgetForm(instance=budget)
        context = {'form': form}
        return render(request, 'mobile/budget/edit.html', context)
    elif request.method == 'POST':
        rotate_token(request)
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            budget = form.save()
            messages.success(request, 'Изменения применены')
            return redirect(to='mobile:budget_list')
        else:
            context = {'form': form}
            return render(request, 'mobile/budget/edit.html', context)


def budget_delete(request, uid):
    from mobile.models import Budget

    budget = get_object_or_404(Budget, id=uid)
    budget.delete()
    messages.warning(request, 'Объект удален')

    return redirect(to='mobile:budget_list')
