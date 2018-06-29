from django.conf.urls import url
from . import views

app_name = 'mobile'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^access_sync_prepare/$', views.access_sync_prepare, name='access_sync_prepare'),
    url(r'^access_sync/$', views.access_sync, name='access_sync'),

    url(r'^sim/new/$', views.sim_new, name='sim_new'),
    url(r'^sim/generate/(?P<bill_id>[0-9]+)/$', views.sim_generate, name='sim_generate'),
    url(r'^sim/(?P<uid>[0-9]+)/$', views.sim_info, name='sim_info', kwargs={'module': 'info'}),
    url(r'^sim/(?P<uid>[0-9]+)/transitions/$', views.sim_info, name='sim_transitions', kwargs={'module': 'transitions'}),
    url(r'^sim/(?P<uid>[0-9]+)/bills/$', views.sim_info, name='sim_bills', kwargs={'module': 'bills'}),
    url(r'^sim/(?P<uid>[0-9]+)/bills/chart/$', views.sim_bills_chart, name='sim_bills_chart'),
    url(r'^sim/(?P<uid>[0-9]+)/limits/$', views.sim_info, name='sim_limits', kwargs={'module': 'limits'}),
    url(r'^sim/(?P<uid>[0-9]+)/edit/$', views.sim_edit, name='sim_edit'),
    url(r'^sim/(?P<uid>[0-9]+)/delete/$', views.sim_delete, name='sim_delete'),
    url(r'^sim/list/$', views.sim_list, name='sim_list'),
    url(r'^sim/list/inactive/$', views.sim_list, name='sim_list_inactive', kwargs={'show_inactive': True}),

    url(r'^transition/new/$', views.transition_new, name='transition_new'),
    url(r'^transition/new/(?P<uid>[0-9]+)/$', views.transition_new, name='transition_new'),
    url(r'^transition/edit/(?P<uid>[0-9]+)/$', views.transition_edit, name='transition_edit'),
    url(r'^transition/delete/(?P<uid>[0-9]+)/$', views.transition_delete, name='transition_delete'),
    url(r'^transition/list/$', views.transition_list, name='transition_list'),

    url(r'^limit/new/$', views.limit_new, name='limit_new'),
    url(r'^limit/new/(?P<uid>[0-9]+)/$', views.limit_new, name='limit_new'),
    url(r'^limit/edit/(?P<uid>[0-9]+)/$', views.limit_edit, name='limit_edit'),
    url(r'^limit/delete/(?P<uid>[0-9]+)/$', views.limit_delete, name='limit_delete'),

    url(r'^contract/new/$', views.contract_new, name='contract_new'),
    url(r'^contract/(?P<uid>[0-9]+)/$', views.contract_info, name='contract_info'),
    url(r'^contract/(?P<uid>[0-9]+)/edit/$', views.contract_edit, name='contract_edit'),
    url(r'^contract/delete/(?P<uid>[0-9]+)/$', views.contract_delete, name='contract_delete'),
    url(r'^contract/list/$', views.contract_list, name='contract_list'),
    url(r'^contract/list/all/$', views.contract_list, name='contract_list_all', kwargs={'show_all': True}),

    url(r'^tariff/new/$', views.tariff_new, name='tariff_new'),
    url(r'^tariff/(?P<uid>[0-9]+)/$', views.tariff_info, name='tariff_info'),
    url(r'^tariff/(?P<uid>[0-9]+)/edit/$', views.tariff_edit, name='tariff_edit'),
    url(r'^tariff/delete/(?P<uid>[0-9]+)/$', views.tariff_delete, name='tariff_delete'),
    url(r'^tariff/list/$', views.tariff_list, name='tariff_list'),

    url(r'^budget/new/$', views.budget_new, name='budget_new'),
    #url(r'^budget/(?P<uid>[0-9]+)/$', views.budget_info, name='budget_info'),
    url(r'^budget/(?P<uid>[0-9]+)/edit/$', views.budget_edit, name='budget_edit'),
    url(r'^budget/delete/(?P<uid>[0-9]+)/$', views.budget_delete, name='budget_delete'),
    url(r'^budget/list/$', views.budget_list, name='budget_list'),

    url(r'^bill/upload/$', views.bill_file_upload, name='bill_upload'),
    url(r'^bill/file_list/$', views.bill_file_list, name='bill_file_list'),
    url(r'^bill/file_info/(?P<uid>[0-9]+)/$', views.bill_file_info, name='bill_file_info'),
    url(r'^bill/file_edit/(?P<uid>[0-9]+)/$', views.bill_file_edit, name='bill_file_edit'),
    url(r'^bill/file_delete/(?P<uid>[0-9]+)/$', views.bill_file_delete, name='bill_file_delete'),
    url(r'^bill/file_refresh/(?P<uid>[0-9]+)/$', views.bill_file_refresh, name='bill_file_refresh'),
    url(r'^bill/file_link_all/(?P<uid>[0-9]+)/$', views.bill_file_link_all, name='bill_file_link_all'),

    url(r'^report/general/$', views.reports.general_report_form, name='general_report_form'),
    url(r'^report/general/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.reports.general_report, name='general_report'),
    url(r'^report/limit/$', views.reports.limit_report_form, name='limit_report_form'),
    url(r'^report/limit/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.reports.limit_report, name='limit_report'),
]
