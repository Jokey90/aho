from django import forms


class YearSelectForm(forms.Form):
    YEARS = (
        (2012, '2012'),
        (2013, '2013'),
        (2014, '2014'),
        (2015, '2015'),
        (2016, '2016'),
        (2017, '2017'),
        (2018, '2018'),
    )

    year = forms.ChoiceField(choices=YEARS, required=True, label='Год')
    year.widget.attrs['class'] = 'narrow'
