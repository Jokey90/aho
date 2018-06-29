from django.forms import ModelForm
from td.models import ItemTracking
from django.contrib.admin import widgets


class ItemMoveForm(ModelForm):

    def __init__(self, *args, **kwargs):
        from td.models import Driver, Item
        new = kwargs.pop('new', False)
        super(ItemMoveForm, self).__init__(*args, **kwargs)
        if new:
            self.fields['owner'].queryset = Driver.objects.filter(active=True)
            self.fields['item'].queryset = Item.objects.filter(active=True)
        else:
            self.fields['item'].disabled = True

    class Meta:
        model = ItemTracking
        fields = [
            'item',
            'owner',
            'date',
        ]

        widgets = {
            'date': widgets.AdminDateWidget(),
        }
