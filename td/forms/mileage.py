from django.forms import ModelForm
from td.models import Mileage


class MileageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from td.models import Car
        new = kwargs.pop('new', False)
        super(MileageForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['car'].queryset = Car.objects.filter(active=True)

    class Meta:
        model = Mileage
        fields = [
            'car',
            'year',
            'month',
            'value',
            'gasoline'
        ]
