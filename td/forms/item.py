from django.forms import ModelForm
from td.models import Item
from django.contrib.admin import widgets


class DocForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from td.models import Car
        new = kwargs.pop('new', False)
        super(DocForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['car'].queryset = Car.objects.filter(active=True)

    class Meta:
        model = Item
        fields = [
            'type',
            'car',
            'number',
            'start_date',
            'end_date',
            'comment',
            'scan'
        ]

        widgets = {
            'start_date': widgets.AdminDateWidget(),
            'end_date': widgets.AdminDateWidget(),
        }


class EnsuranceForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from td.models import Car
        new = kwargs.pop('new', False)
        super(EnsuranceForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['car'].queryset = Car.objects.filter(active=True)

    class Meta:
        model = Item
        fields = [
            'type',
            'car',
            'number',
            'start_date',
            'end_date',
            'company',
            'comment',
            'scan'
        ]

        widgets = {
            'start_date': widgets.AdminDateWidget(),
            'end_date': widgets.AdminDateWidget(),
        }


class KeyForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from td.models import Car
        new = kwargs.pop('new', False)
        super(KeyForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['car'].queryset = Car.objects.filter(active=True)

    class Meta:
        model = Item
        fields = [
            'type',
            'car',
            'number',
            'pin',
            'comment',
            'scan'
        ]
