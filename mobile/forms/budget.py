from django import forms
from mobile.models import Budget
from django.contrib.admin import widgets


class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget
        fields = [
            'year',
            'division',
            'amount'
        ]
