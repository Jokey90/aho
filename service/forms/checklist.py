from django import forms
from service.models import Checklist, ChecklistValue
from service.widgets import *


class ChecklistNewForm(forms.ModelForm):

    class Meta:
        model = Checklist
        fields = [
            'date',
            'floor'
        ]
        widgets = {
            'date': DateInput()
        }


class ChecklistValueForm(forms.ModelForm):

    class Meta:
        model = ChecklistValue
        fields = [
            'row',
            'has_issues',
            'photo',
            'comment'
        ]
        widgets = {
            'has_issues': Checkbox(),
            'row': forms.HiddenInput(),
            'photo': FileInput()
        }


class ChecklistValueEditForm(forms.ModelForm):

    class Meta:
        model = ChecklistValue
        fields = [
            'has_issues',
            'solve_date',
            'photo',
            'comment'
        ]

        widgets = {
            'has_issues': Checkbox(),
            'solve_date': DateInput()
        }


class ChecklistEditForm(forms.ModelForm):

    class Meta:
        model = Checklist
        fields = [
            'date',
            'floor'
        ]
        widgets = {
            'date': DateInput()
        }


class ChecklistValueEditInlineForm(forms.ModelForm):

    class Meta:
        model = ChecklistValue
        fields = [
            'id',
            'has_issues',
            'solve_date',
            'photo',
            'comment'
        ]

        widgets = {
            'id': forms.HiddenInput(),
            'has_issues': Checkbox(),
            'solve_date': DateInput(),
            'photo': FileInput()
        }


class ChecklistValueSolveForm(forms.ModelForm):

    class Meta:
        model = ChecklistValue
        fields = [
            'solve_date'
        ]
        widgets = {
            'solve_date': DateInput()
        }

    close_ticket = forms.BooleanField(label='Закрыть связанную заявку той же датой', widget=Checkbox(), required=False)
