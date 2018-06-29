from django.db import models


class Item(models.Model):
    from td.models import Car

    class Meta:
        verbose_name = 'Документ/ключ/пропуск'
        verbose_name_plural = 'Документы/ключи/пропуска'

    TYPES = [
        ('doc', 'pts', 'ПТС'),
        ('doc', 'sts', 'СТС'),
        ('doc', 'diag_card', 'Диагностическая карта'),
        ('doc', 'fuel_card', 'Топливная карта'),
        ('doc', 'corp_card', 'Корпоративная карта'),
        ('doc', 'service_book', 'Сервисная книжка'),
        ('ensurance', 'osago', 'Полис ОСАГО'),
        ('ensurance', 'kasko', 'Полис КАСКО'),
        ('key', 'key-car', 'Ключ от автомобиля'),
        ('key', 'key-alarm', 'Ключ от сигнализации'),
        ('key', 'key-card', 'Ключ-карта'),
        ('key', 'key-parking', 'Пропуск на парковку'),
    ]

    type = models.CharField(verbose_name='Тип', blank=False, null=False, choices=[(x[1], x[2]) for x in TYPES], max_length=50)
    car = models.ForeignKey(verbose_name='Автомобиль', to=Car, blank=False, null=False)
    number = models.CharField(verbose_name='Номер', blank=True, null=True, default='', max_length=50)
    pin = models.CharField(verbose_name='Пин код', blank=True, null=True, default='', max_length=50)
    start_date = models.DateField(verbose_name='Дата начала', blank=True, null=True)
    end_date = models.DateField(verbose_name='Дата окончания', blank=True, null=True)
    company = models.CharField(verbose_name='Компания', blank=True, null=True, default='', max_length=50)
    comment = models.CharField(verbose_name='Комментарий', blank=True, null=True, default='', max_length=255)
    active = models.BooleanField(verbose_name='Активен', blank=False, null=False, default=True)
    scan = models.FileField(verbose_name='Скан', blank=True, upload_to='scans/car_items/', null=True)

    def __str__(self):
        return self.get_type_display() + ' ' + self.number # + ' ' + self.car.name + ' ' + self.car.number

    def get_type(self):
        for type in Item.TYPES:
            if type[1] == self.type:
                return type[0]
        else:
            return None

    def current_owner(self):
        from td.models import ItemTracking
        from datetime import date
        last_moves = ItemTracking.objects.filter(item=self, date__lte=date.today()).order_by('-date', '-id')
        if len(last_moves) > 0:
            return last_moves.first().owner
        else:
            return None

    def get_last_move(self):
        from td.models import ItemTracking
        from datetime import date
        last_moves = ItemTracking.objects.filter(item=self, date__lte=date.today()).order_by('-date', '-id')
        if len(last_moves) > 0:
            return last_moves.first().date
        else:
            return None

    def former_owner(self, date):
        from td.models import ItemTracking
        last_moves = ItemTracking.objects.filter(item=self, date__lte=date).order_by('-date', '-id')
        if len(last_moves) > 0:
            return last_moves.first().owner
        else:
            return None
