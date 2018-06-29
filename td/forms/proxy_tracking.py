from django.forms import ModelForm
from td.models import ProxyTracking
from django.contrib.admin import widgets


class ProxyMoveForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from td.models import Driver, Proxy
        new = kwargs.pop('new', False)
        super(ProxyMoveForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['owner'].queryset = Driver.objects.filter(active=True)
            self.fields['proxy'].queryset = Proxy.objects.filter(active=True)
        else:
            self.fields['proxy'].disabled = True

    class Meta:
        model = ProxyTracking
        fields = [
            'proxy',
            'owner',
            'date',
        ]

        widgets = {
            'date': widgets.AdminDateWidget(),
        }
