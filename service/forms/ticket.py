from django import forms
from service.models import Ticket
from service.widgets import *


class TicketNewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        from service.models import ChecklistValue
        super(TicketNewForm, self).__init__(*args, **kwargs)
        self.fields['issue'].queryset = ChecklistValue.objects.filter(has_issues=True, solve_date__isnull=True).order_by('-checklist__date', '-checklist__floor__name', 'row__zone__ord_number')

    class Meta:
        model = Ticket
        widgets = {
            'text': forms.Textarea(attrs={'cols': '60', 'rows': '10'})
        }
        fields = [
            'subject',
            'provider',
            'photo',
            'text',
            'issue'
        ]

    attach_file = forms.BooleanField(label='Прикрепить фото из замечания', widget=Checkbox(), required=False)


class TicketEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        from service.models import ChecklistValue
        super(TicketEditForm, self).__init__(*args, **kwargs)
        self.fields['issue'].queryset = ChecklistValue.objects.filter(has_issues=True, solve_date__isnull=True).order_by('-checklist__date', '-checklist__floor__name', 'row__zone__ord_number')

    class Meta:
        model = Ticket
        fields = [
            'subject',
            'provider',
            'photo',
            'text',
            'issue'
        ]
        widgets = {
            'text': forms.Textarea(attrs={'cols': '60', 'rows': '10'})
        }


class TicketColseForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = [
            'close_date'
        ]
        widgets = {
            'close_date': DateInput()
        }

    solve_issue = forms.BooleanField(label='Устранить связанное замечание той же датой', widget=Checkbox(), required=False)