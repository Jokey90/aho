from django.forms import ModelForm
from td.models import Parking
from django.contrib.admin import widgets


class ParkingForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from main.models import Employee
        new = kwargs.pop('new', False)
        super(ParkingForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['owner'].queryset = Employee.objects.filter(active=True)

    class Meta:
        model = Parking
        fields = [
            'number',
            'car_name',
            'owner',
            'payment_type',
            'contract',
            'contract_date',
            'floor_number',
            'grade',
            'basis',
            'comment'
        ]

        widgets = {
            'contract_date': widgets.AdminDateWidget()
        }