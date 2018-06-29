from django.forms import ModelForm
from django import forms
from td.models import Proxy
from django.contrib.admin import widgets


class ProxyForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from td.models import Driver, Car
        new = kwargs.pop('new', False)
        super(ProxyForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['driver'].queryset = Driver.objects.filter(active=True)
            self.fields['car'].queryset = Car.objects.filter(active=True)

    class Meta:
        model = Proxy
        fields = [
            'car',
            'driver',
            'start_date',
            'end_date',
            'type',
            'scan'
        ]
        widgets = {
            'start_date': widgets.AdminDateWidget(),
            'end_date': widgets.AdminDateWidget()
        }
