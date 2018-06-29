from django.forms import ModelForm
from td.models import AccidentDoc
from django.contrib.admin import widgets


class AccidentDocForm(ModelForm):

    class Meta:
        model = AccidentDoc
        fields = [
            'name',
            'accident',
            'scan'
        ]
