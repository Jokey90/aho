from django import forms
from service.models import Provider
from service.widgets import *


class ProviderEditForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = [
            'name',
            'contact'
        ]
