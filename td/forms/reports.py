from django import forms

from main.structures import MONTHS


class YearSelectForm(forms.Form):
    YEARS = (
        (2016, '2016'),
        (2017, '2017'),
        (2018, '2018'),
    )

    year = forms.ChoiceField(choices=YEARS, required=True, label='Год')
    year.widget.attrs['class'] = 'narrow'


class YearMonthSelectForm(forms.Form):
    YEARS = (
        (2016, '2016'),
        (2017, '2017'),
        (2018, '2018'),
    )

    month = forms.ChoiceField(choices=MONTHS, required=True, label='Месяц')
    year = forms.ChoiceField(choices=YEARS, required=True, label='Год')

    month.widget.attrs['class'] = 'narrow'
    year.widget.attrs['class'] = 'narrow'


class CarSelectForm(forms.Form):
    from td.models import Car

    cars = []
    for car in Car.objects.filter(active=True).all():
        cars.append([car.id, str(car)])

    car = forms.ChoiceField(choices=cars, required=True, label='Автомобиль')

    car.widget.attrs['class'] = 'narrow2'


class DriverSelectForm(forms.Form):
    from td.models import Driver

    drivers = []
    for driver in Driver.objects.filter(active=True).all():
        drivers.append([driver.id, str(driver)])

    driver = forms.ChoiceField(choices=drivers, required=True, label='Водитель')

    driver.widget.attrs['class'] = 'narrow2'


class CarDriverPeriodForm(forms.Form):
    from td.models import Car
    from td.models import Driver
    from django.contrib.admin.widgets import AdminDateWidget

    cars = [[0, 'Все']]
    for car in Car.objects.filter(active=True).all():
        cars.append([car.id, str(car)])

    drivers = [[0, 'Все']]
    for driver in Driver.objects.filter(active=True).all():
        drivers.append([driver.id, str(driver)])

    car = forms.ChoiceField(choices=cars, required=True, label='Автомобиль')
    driver = forms.ChoiceField(choices=drivers, required=True, label='Водитель')
    start_date = forms.DateField(widget=AdminDateWidget(), label='Начало периода', required=False)
    end_date = forms.DateField(widget=AdminDateWidget(), label='Конец периода', required=False)

    car.widget.attrs['class'] = 'narrow2'
    driver.widget.attrs['class'] = 'narrow2'


class CarPeriodForm(forms.Form):
    from td.models import Car
    from django.contrib.admin.widgets import AdminDateWidget

    cars = [[0, 'Все']]
    for car in Car.objects.filter(active=True).all():
        cars.append([car.id, str(car)])

    car = forms.ChoiceField(choices=cars, required=True, label='Автомобиль')
    start_date = forms.DateField(widget=AdminDateWidget(), label='Начало периода', required=False)
    end_date = forms.DateField(widget=AdminDateWidget(), label='Конец периода', required=False)

    car.widget.attrs['class'] = 'narrow2'


class PeriodForm(forms.Form):
    from django.contrib.admin.widgets import AdminDateWidget

    start_date = forms.DateField(widget=AdminDateWidget(), label='Начало периода', required=False)
    end_date = forms.DateField(widget=AdminDateWidget(), label='Конец периода', required=False)
