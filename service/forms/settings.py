from django import forms
from main.models import GlobalSettings
from service.widgets import *


class GlobalSettingsForm(forms.ModelForm):

    class Meta:
        model = GlobalSettings
        fields = [
            'id',
            'value'
        ]
        widgets = {
            'id': forms.HiddenInput(),
            'value': forms.Textarea(attrs={'cols': '60', 'rows': '5'})
        }
