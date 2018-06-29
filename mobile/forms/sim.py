from django import forms
from mobile.models import Sim


class SimForm(forms.ModelForm):

    '''def __init__(self, *args, **kwargs):
        from td.models import Car
        new = kwargs.pop('new', False)
        super(MileageForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['car'].queryset = Car.objects.filter(active=True)'''

    class Meta:
        model = Sim
        fields = [
            'number',
            'tariff',
            'comment'
        ]


class SimSearchForm(forms.Form):
    search = forms.CharField(label='Строка поиска', initial='', help_text='Поиск')
    search.widget.attrs['placeholder'] = 'Поиск'
