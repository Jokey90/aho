from django import forms
from main.models import Contact


class ContactEditForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = [
            'name',
            'address',
            'person_name',
            'email',
            'phone_number',
            'comment'
        ]
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3})
        }
