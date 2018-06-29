from django.db import models
from main.models.employee import Employee


class Car(models.Model):

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    active = models.BooleanField(verbose_name='Активен', blank=False, null=False, default=True)
    drivers = models.ManyToManyField(verbose_name='Ответственный/водитель', to='Driver', blank=True,
                                     related_name='cars_driven', through='Proxy')

    # common properties:

    name = models.CharField(verbose_name='Модель', max_length=100, blank=False, null=False)
    number = models.CharField(verbose_name='Гос. номер', max_length=20, default='', blank=False, null=False)
    vin = models.CharField(verbose_name='VIN', max_length=50, blank=True, null=True)
    description = models.CharField(verbose_name='Описание/комментарии', max_length=1000, blank=True, null=True)
    owner = models.ForeignKey(verbose_name='Руководитель/пассажир', to=Employee, blank=True, null=True, related_name='cars_owned')
    release_year = models.IntegerField(verbose_name='Год выпуска', default=2000, blank=True, null=True)

    power = models.IntegerField(verbose_name='Мощность, л.с.', default=0, blank=True, null=True)
    engine_volume = models.FloatField(verbose_name='Объем двигателя, л', default=0, blank=True, null=True)

    to_mileage = models.IntegerField(verbose_name='Пробег между ТО', default=0, blank=True, null=True)
    mileage_limit = models.IntegerField(verbose_name='Ограничение пробега', blank=True, null=True)

    FUEL_TYPES = (
        ('0', 'Бензин'),
        ('1', 'Дизель')
    )
    fuel_type = models.CharField(verbose_name='Тип топлива', choices=FUEL_TYPES, default='0', max_length=1, blank=True, null=True)

    # documents:

    DOC_STATES = (
        ('0', 'нет / не должно быть'),
        ('1', 'оригинал в машине/на руках у водителей'),
        ('2', 'оригинал в бухгалтерии'),
        ('3', 'оригинал в архиве, документ не действительный'),
    )

    alarm_number = models.CharField(verbose_name='Номер маяка сигнализации', default='', max_length=50, blank=True, null=True)
    alarm_sim_number = models.CharField(verbose_name='Номер SIM-карты маяка', default='', max_length=50, blank=True, null=True)

    # tires into

    TIRES_STATES = (
        ('0', 'да'),
        ('1', 'да (с дисками)'),
        ('2', 'нет'),
        ('3', 'нет (диски есть)'),
    )

    TIRES_STORAGES = (
        ('0', ' '),
        ('1', 'Динамика М'),
        ('2', 'У водителя в гараже/дома'),
        ('3', 'ТРК Щука'),
        ('4', 'Стенд-авто'),
    )

    tires_storage = models.CharField(verbose_name='Место хранения колес', choices=TIRES_STORAGES, max_length=1, default='0', blank=True, null=True)

    tires_summer_state = models.CharField(verbose_name='Летние колеса, наличие', choices=TIRES_STATES, blank=True, null=True, default='0', max_length=1)
    tires_summer_date = models.DateField(verbose_name='Летние колеса, срок действия', blank=True, null=True)
    tires_summer_photo = models.FileField(verbose_name='Летние колеса, фото', blank=True, null=True, upload_to='photos/tires/')

    tires_winter_state = models.CharField(verbose_name='Зимние колеса, наличие', choices=TIRES_STATES, blank=True, null=True, default='0', max_length=1)
    tires_winter_date = models.DateField(verbose_name='Зимние колеса, срок действия', blank=True, null=True)
    tires_winter_photo = models.FileField(verbose_name='Зимние колеса, фото', blank=True, null=True, upload_to='photos/tires/')

    tires_comment = models.CharField(verbose_name='Комментарии к колесам', blank=True, null=True, max_length=255)

    # keys info

    vip_pass = models.BooleanField(verbose_name='VIP-пропуск', default=False, blank=False, null=False)

    # ownership info

    OWNERSHIP_TYPES = (
        ('0', 'Собственность ГОРН'),
        ('1', 'Собственность ФЛ, в аренде ГОРН'),
        ('2', 'Собственность ФЛ'),
    )

    ownership_type = models.CharField(verbose_name='Тип собственности', choices=OWNERSHIP_TYPES, default='0', max_length=1, blank=False, null=False)
    rent_contract = models.CharField(verbose_name='Договор аренды автотранспортного средства без экипажа', choices=DOC_STATES, default='0', max_length=1, blank=False, null=False)
    rent_contract2 = models.CharField(verbose_name='Договор на предоставление информационных, диспетчерских и технологических услуг', choices=DOC_STATES, default='0', max_length=1, blank=False, null=False)

    def __str__(self):
        return self.name + ' ' + self.number
