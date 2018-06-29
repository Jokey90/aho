from django.forms import ModelForm
from td.models import Expense
from django.contrib.admin import widgets


class ExpenseForm(ModelForm):

    class Meta:
        model = Expense
        fields = [
            'date',
            'car',
            'driver',
            'budget_subitem',
            'amount',
            'comment'
        ]
        widgets = {
            'date': widgets.AdminDateWidget()
        }