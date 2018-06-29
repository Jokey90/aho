from django.forms import ModelForm
from django import forms
from main.models import Employee


class EmployeeForm(ModelForm):

    class Meta:
        model = Employee

        fields = [
            'last_name',
            'first_name',
            'middle_name',
            'department',
            'position',
            'group',
            'active'
        ]