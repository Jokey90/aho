from django.db import models
from td.models import Item, Driver
from django.contrib.auth.models import User


class ItemTracking(models.Model):

    class Meta:
        verbose_name = 'Выдача документов/ключей'
        verbose_name_plural = 'Выдачи документов/ключей'

    item = models.ForeignKey(verbose_name='Объект',to=Item, blank=False, null=False)
    owner = models.ForeignKey(verbose_name='Кому выдан', to=Driver, blank=False, null=False)
    date = models.DateField(verbose_name='Дата передачи', blank=False, null=False)
    added_by = models.ForeignKey(to=User, blank=False, null=False)
    add_date = models.DateTimeField(auto_now_add=True)

    def last_owner(self):
        prev_tracks = ItemTracking.objects.filter(item=self.item, item__active=True, date__lte=self.date).exclude(id=self.id).order_by('-date', '-id')
        if len(prev_tracks) > 0:
            return prev_tracks.first().owner
        else:
            return None
