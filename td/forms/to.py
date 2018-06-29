from django.forms import ModelForm
from django import forms
from td.models import TO
from django.contrib.admin import widgets


class TOForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from td.models import Car
        new = kwargs.pop('new', False)
        super(TOForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['car'].queryset = Car.objects.filter(active=True)

    class Meta:
        model = TO
        fields = [
            'name',
            'car',
            'date',
            'mileage',
            'budget_amount',
            'fact_amount',
            'comment'
        ]
        widgets = {
            'date': widgets.AdminDateWidget()
        }
