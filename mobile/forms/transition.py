from django import forms
from mobile.models import Transition
from django.contrib.admin import widgets


class TransitionForm(forms.ModelForm):

    class Meta:
        model = Transition
        fields = [
            'sim',
            'employee',
            'comment'
        ]
        exclude = ['date']

    date_field = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())
    date_field.label = 'Дата передачи'
