from django.forms import ModelForm
from td.models import Accident
from django.contrib.admin import widgets


class AccidentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from td.models import Car, Driver
        new = kwargs.pop('new', False)
        super(AccidentForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['car'].queryset = Car.objects.filter(active=True)
            self.fields['culprit'].queryset = Driver.objects.filter(active=True)

    class Meta:
        model = Accident
        fields = [
            'name',
            'date',
            'car',
            'culprit',
            'comment'
        ]

        widgets = {
            'date': widgets.AdminDateWidget()
        }
