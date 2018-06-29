from django.forms import ModelForm
from td.models import Penalty
from django.contrib.admin import widgets


class PenaltyForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from td.models import Car, Driver
        new = kwargs.pop('new', False)
        super(PenaltyForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['driver'].queryset = Driver.objects.filter(active=True)
            self.fields['car'].queryset = Car.objects.filter(active=True)

    class Meta:
        model = Penalty
        fields = [
            'date',
            'car',
            'driver',
            'description',
            'number',
            'amount',
            'scan',
            'obtain_date',
            'payed',
            'pay_date'
        ]
        widgets = {
            'date': widgets.AdminDateWidget(),
            'obtain_date': widgets.AdminDateWidget(),
            'pay_date': widgets.AdminDateWidget(),
        }