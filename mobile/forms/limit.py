from django import forms
from mobile.models import Limit
from django.contrib.admin import widgets


class LimitForm(forms.ModelForm):

    class Meta:
        model = Limit
        fields = [
            'sim',
            'amount',
            'infinite',
            'date'
        ]
        widgets = {
            'date': widgets.AdminDateWidget()
        }
