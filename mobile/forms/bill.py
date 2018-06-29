from django import forms
from mobile.models import BillFile


class BillFileForm(forms.ModelForm):

    class Meta:
        model = BillFile
        fields = [
            'name',
            'year',
            'month',
            'file'
        ]


class BillFileEditForm(forms.ModelForm):

    class Meta:
        model = BillFile
        fields = [
            'name',
            'year',
            'month'
        ]