from django.forms import ModelForm
from django import forms
from td.models import Driver
from django.contrib.admin import widgets


class DriverForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from main.models import Employee
        new = kwargs.pop('new', False)
        super(DriverForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['emp'].queryset = Employee.objects.filter(active=True)

    class Meta:
        model = Driver
        fields = [
            'emp',
            'license',
            'license_date',
            'phone',
            'photo',
            'comment'
        ]

        widgets = {
            'license_date': widgets.AdminDateWidget()
        }
