from django.conf.urls import url
from . import views

app_name = 'service'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^checklist/new/$', views.checklist_new, name='checklist_new'),
    url(r'^checklist/(?P<uid>[0-9]+)/$', views.checklist_info, name='checklist_info'),
    url(r'^checklist/(?P<uid>[0-9]+)/xls/$', views.checklist_xls, name='checklist_xls'),
    url(r'^checklist/(?P<uid>[0-9]+)/edit/$', views.checklist_edit, name='checklist_edit'),
    url(r'^checklist/list/with_issues/$', views.checklist_list, name='checklist_list', kwargs={'state': 'issues'}),
    url(r'^checklist/list/solved/$', views.checklist_list, name='checklist_list', kwargs={'state': 'solved'}),
    url(r'^checklist/list/$', views.checklist_list, name='checklist_list'),

    url(r'^checklist_value/(?P<uid>[0-9]+)/$', views.checklist_value_info, name='checklist_value_info'),
    url(r'^checklist_value/(?P<uid>[0-9]+)/solve/$', views.checklist_value_solve, name='checklist_value_solve'),
    url(r'^checklist_value/(?P<uid>[0-9]+)/edit/$', views.checklist_value_edit, name='checklist_value_edit'),
    url(r'^checklist_value/list/unsolved/$', views.checklist_value_list, name='checklist_value_list', kwargs={'state': 'unsolved'}),
    url(r'^checklist_value/list/solved/$', views.checklist_value_list, name='checklist_value_list', kwargs={'state': 'solved'}),
    url(r'^checklist_value/list/$', views.checklist_value_list, name='checklist_value_list'),

    url(r'^provider/list/$', views.provider_list, name='provider_list'),
    url(r'^provider/(?P<uid>[0-9]+)/info/$', views.provider_info, name='provider_info'),
    url(r'^provider/new/$', views.provider_new, name='provider_new'),
    url(r'^provider/(?P<uid>[0-9]+)/edit/$', views.provider_edit, name='provider_edit'),

    url(r'^ticket/new/$', views.ticket_new, name='ticket_new'),
    url(r'^ticket/(?P<uid>[0-9]+)/info/$', views.ticket_info, name='ticket_info'),
    url(r'^ticket/(?P<uid>[0-9]+)/edit/$', views.ticket_edit, name='ticket_edit'),
    url(r'^ticket/(?P<uid>[0-9]+)/close/$', views.ticket_close, name='ticket_close'),
    url(r'^ticket/(?P<uid>[0-9]+)/resend_email/$', views.ticket_resend_email, name='ticket_resend_email'),
    url(r'^ticket/list/closed/$', views.ticket_list, name='ticket_list', kwargs={'state': 'closed'}),
    url(r'^ticket/list/active/$', views.ticket_list, name='ticket_list', kwargs={'state': 'active'}),
    url(r'^ticket/list/$', views.ticket_list, name='ticket_list'),

    url(r'^settings/$', views.settings, name='settings'),
]
