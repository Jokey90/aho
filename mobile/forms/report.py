from django import forms
from mobile.models import Limit
from django.contrib.admin import widgets


class GeneralReportForm(forms.Form):
    from main.structures import MONTHS
    from datetime import date

    month = forms.ChoiceField(choices=MONTHS, initial=date.today().month, label='Месяц')
    year = forms.IntegerField(min_value=2012, max_value=2099, initial=date.today().year, label='Год')


class LimitReportForm(forms.Form):
    from main.structures import MONTHS
    from datetime import date

    month = forms.ChoiceField(choices=MONTHS, initial=date.today().month, label='Месяц')
    year = forms.IntegerField(min_value=2012, max_value=2099, initial=date.today().year, label='Год')
