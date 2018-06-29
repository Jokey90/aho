from django.forms import ModelForm
from django import forms
from main.models import Department


class DepartmentForm(ModelForm):

    class Meta:
        model = Department
        fields = [
            'name',
            'description',
            'parent_department',
            'division'
        ]