from django import forms
from mobile.models import Tariff
from django.contrib.admin import widgets


class TariffForm(forms.ModelForm):

    class Meta:
        model = Tariff
        fields = [
            'name',
            'description'
        ]
