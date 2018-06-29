from django.db import models
from td.models import Proxy, Driver
from django.contrib.auth.models import User


class ProxyTracking(models.Model):

    class Meta:
        verbose_name = 'Выдача доверенности'
        verbose_name_plural = 'Выдачи доверенностей'

    proxy = models.ForeignKey(verbose_name='Доверенность',to=Proxy, blank=False, null=False)
    owner = models.ForeignKey(verbose_name='Кому выдана', to=Driver, blank=False, null=False)
    date = models.DateField(verbose_name='Дата передачи', blank=False, null=False)
    added_by = models.ForeignKey(to=User, blank=False, null=False)
    add_date = models.DateTimeField(auto_now_add=True)

    def last_owner(self):
        prev_tracks = ProxyTracking.objects.filter(proxy=self.proxy, proxy__active=True, date__lte=self.date).exclude(id=self.id).order_by('-date', '-id')
        if len(prev_tracks) > 0:
            return prev_tracks.first().owner
        else:
            return None
