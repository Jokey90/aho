from django.forms import ModelForm
from td.models import VisitorsParking
from django.contrib.admin import widgets


class VisitorsParkingForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from main.models import Employee
        new = kwargs.pop('new', False)
        super(VisitorsParkingForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['invited_by'].queryset = Employee.objects.filter(active=True)

    class Meta:
        model = VisitorsParking
        fields = [
            'date',
            'time',
            'end_time',
            'visitors_name',
            'car_number',
            'invited_by',
            'comment'
        ]
        widgets = {
            'date': widgets.AdminDateWidget(),
            'time': widgets.AdminTimeWidget(),
            'end_time': widgets.AdminTimeWidget(),
        }