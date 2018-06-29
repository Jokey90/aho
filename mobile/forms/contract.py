from django import forms
from mobile.models import Contract
from django.contrib.admin import widgets


class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = [
            'name',
            'number',
            'group',
            'mts',
            'comment'
        ]
