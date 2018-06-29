from django.forms import ModelForm
from django import forms
from td.models import Car
from django.contrib.admin import widgets


class CarNewForm(ModelForm):

    class Meta:
        model = Car
        fields = [
            'name',
            'number',
            'description',
            'ownership_type',
        ]


class CarEditInfoForm(ModelForm):

    class Meta:
        model = Car
        fields = [
            'name',
            'number',
            'vin',
            'description',
            'owner',
            'release_year',
            'power',
            'engine_volume',
            'to_mileage',
            'mileage_limit',
            'vip_pass',
            'alarm_number',
            'alarm_sim_number',
            'ownership_type',
            'rent_contract',
            'rent_contract2',
        ]


class CarEditTiresForm(ModelForm):

    class Meta:
        model = Car
        fields = [
            'tires_storage',
            'tires_comment',
            'tires_summer_state',
            'tires_summer_date',
            'tires_summer_photo',
            'tires_winter_state',
            'tires_winter_date',
            'tires_winter_photo',
        ]

        widgets = {
            'tires_summer_date': widgets.AdminDateWidget(),
            'tires_winter_date': widgets.AdminDateWidget(),
        }