from django.conf.urls import url
from . import views

app_name = 'td'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^car/list/$', views.car_list, name='car_list'),
    url(r'^car/list/inactive/$', views.car_list, name='car_list_inactive', kwargs={'show_inactive': True}),
    url(r'^car/new/$', views.car_new, name='car_new'),
    url(r'^car/(?P<cid>[0-9]+)/info/$', views.car_info, name='car_info', kwargs={'block': 'info'}),
    url(r'^car/(?P<cid>[0-9]+)/edit_info/$', views.car_edit, name='car_edit_info', kwargs={'block': 'info'}),
    url(r'^car/(?P<cid>[0-9]+)/docs/$', views.car_docs, name='car_docs'),
    url(r'^car/(?P<cid>[0-9]+)/ensurance/$', views.car_ensurance, name='car_ensurance'),
    url(r'^car/(?P<cid>[0-9]+)/proxies/$', views.car_proxies, name='car_proxies'),
    url(r'^car/(?P<cid>[0-9]+)/accidents/$', views.car_accidents, name='car_accidents'),
    url(r'^car/(?P<cid>[0-9]+)/penalties/$', views.car_penalties, name='car_penalties'),
    url(r'^car/(?P<cid>[0-9]+)/keys/$', views.car_keys, name='car_keys'),
    url(r'^car/(?P<cid>[0-9]+)/to/$', views.car_to, name='car_to'),
    url(r'^car/(?P<cid>[0-9]+)/tires/$', views.car_info, name='car_tires', kwargs={'block': 'tires'}),
    url(r'^car/(?P<cid>[0-9]+)/edit_tires/$', views.car_edit, name='car_edit_tires', kwargs={'block': 'tires'}),
    url(r'^car/(?P<cid>[0-9]+)/delete/$', views.car_delete, name='car_delete'),
    url(r'^car/(?P<cid>[0-9]+)/mileage/$', views.car_mileage, name='car_mileage'),
    url(r'^car/(?P<cid>[0-9]+)/expenses/$', views.car_expenses, name='car_expenses'),
    url(r'^car/(?P<cid>[0-9]+)/expenses/(?P<year>[0-9]{4})/$', views.car_expenses, name='car_expenses'),
    # url(r'^car/(?P<cid>[0-9]+)/edit_docs/$', views.car_edit, name='car_edit_docs', kwargs={'block': 'docs'}),
    # url(r'^car/(?P<cid>[0-9]+)/edit_ensurance/$', views.car_edit, name='car_edit_ensurance', kwargs={'block': 'ensurance'}),
    # url(r'^car/(?P<cid>[0-9]+)/mileage/$', views.car_mileage, name='car_mileage'),
    # url(r'^car/(?P<cid>[0-9]+)/mileage/(?P<year>[0-9]{4})/$', views.car_mileage, name='car_mileage'),

    url(r'^key/new/$', views.item_new, name='key_new', kwargs={'item_type': 'key'}),
    url(r'^doc/new/$', views.item_new, name='doc_new', kwargs={'item_type': 'doc'}),
    url(r'^ensurance/new/$', views.item_new, name='ensurance_new', kwargs={'item_type': 'ensurance'}),
    url(r'^item/(?P<iid>[0-9]+)/$', views.item_info, name='item_info'),
    url(r'^item/(?P<iid>[0-9]+)/edit/$', views.item_edit, name='item_edit'),
    url(r'^item/(?P<iid>[0-9]+)/delete/$', views.item_delete, name='item_delete'),

    url(r'^item/(?P<iid>[0-9]+)/move/$', views.item_tracking_new, name='item_tracking_new'),
    url(r'^item_tracking/(?P<tid>[0-9]+)/edit/$', views.item_tracking_edit, name='item_tracking_edit'),
    url(r'^item_tracking/(?P<tid>[0-9]+)/delete/$', views.item_tracking_delete, name='item_tracking_delete'),

    url(r'^accident/new/$', views.accident_new, name='accident_new'),
    url(r'^accident/(?P<aid>[0-9]+)/$', views.accident_info, name='accident_info'),
    url(r'^accident/(?P<aid>[0-9]+)/edit/$', views.accident_edit, name='accident_edit'),
    url(r'^accident/(?P<aid>[0-9]+)/delete/$', views.accident_delete, name='accident_delete'),

    url(r'^accident_doc/new/$', views.accident_doc_new, name='accident_doc_new'),
    url(r'^accident_doc/(?P<did>[0-9]+)/$', views.accident_doc_info, name='accident_doc_info'),
    url(r'^accident_doc/(?P<did>[0-9]+)/edit/$', views.accident_doc_edit, name='accident_doc_edit'),
    url(r'^accident_doc/(?P<did>[0-9]+)/delete/$', views.accident_doc_delete, name='accident_doc_delete'),

    url(r'^driver/list/$', views.driver_list, name='driver_list'),
    url(r'^driver/list/inactive/$', views.driver_list, name='driver_list_inactive', kwargs={'show_inactive': True}),
    url(r'^driver/new/$', views.driver_new, name='driver_new'),
    url(r'^driver/(?P<did>[0-9]+)/$', views.driver_info, name='driver_info'),
    url(r'^driver/(?P<did>[0-9]+)/edit/$', views.driver_edit, name='driver_edit'),
    url(r'^driver/(?P<did>[0-9]+)/delete/$', views.driver_delete, name='driver_delete'),

    url(r'^proxy/list/$', views.proxy_list, name='proxy_list'),
    url(r'^proxy/list/inactive/$', views.proxy_list, name='proxy_list_inactive', kwargs={'show_inactive': True}),
    url(r'^proxy/new/$', views.proxy_new, name='proxy_new'),
    url(r'^proxy/(?P<pid>[0-9]+)/$', views.proxy_info, name='proxy_info'),
    url(r'^proxy/(?P<pid>[0-9]+)/edit/$', views.proxy_edit, name='proxy_edit'),
    url(r'^proxy/(?P<pid>[0-9]+)/delete/$', views.proxy_delete, name='proxy_delete'),

    url(r'^proxy/(?P<pid>[0-9]+)/move/$', views.proxy_tracking_new, name='proxy_tracking_new'),
    url(r'^proxy_tracking/(?P<tid>[0-9]+)/edit/$', views.proxy_tracking_edit, name='proxy_tracking_edit'),
    url(r'^proxy_tracking/(?P<tid>[0-9]+)/delete/$', views.proxy_tracking_delete, name='proxy_tracking_delete'),

    url(r'^to/list/$', views.to_list, name='to_list'),
    url(r'^to/new/$', views.to_new, name='to_new'),
    url(r'^to/(?P<tid>[0-9]+)/$', views.to_info, name='to_info'),
    url(r'^to/(?P<tid>[0-9]+)/edit/$', views.to_edit, name='to_edit'),
    url(r'^to/(?P<tid>[0-9]+)/delete/$', views.to_delete, name='to_delete'),

    url(r'^mileage/list/$', views.mileage_list, name='mileage_list'),
    url(r'^mileage/new/$', views.mileage_new, name='mileage_new'),
    url(r'^mileage/(?P<mid>[0-9]+)/$', views.mileage_info, name='mileage_info'),
    url(r'^mileage/(?P<mid>[0-9]+)/edit/$', views.mileage_edit, name='mileage_edit'),
    url(r'^mileage/(?P<mid>[0-9]+)/delete/$', views.mileage_delete, name='mileage_delete'),

    url(r'^budget/list/$', views.budget_list, name='budget_list'),
    url(r'^budget/list/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<item>[0-9]+)/$', views.budget_details, name='budget_details'),
    url(r'^budget/list/(?P<year>[0-9]{4})/(?P<item>[0-9]+)/$', views.budget_subitem_details, name='budget_subitem_details'),

    url(r'^expense/list/$', views.expense_list, name='expense_list'),
    url(r'^expense/new/$', views.expense_new, name='expense_new'),
    url(r'^expense/(?P<eid>[0-9]+)/$', views.expense_info, name='expense_info'),
    url(r'^expense/(?P<eid>[0-9]+)/edit/$', views.expense_edit, name='expense_edit'),
    url(r'^expense/(?P<eid>[0-9]+)/delete/$', views.expense_delete, name='expense_delete'),

    url(r'^penalty/list/$', views.penalty_list, name='penalty_list'),
    url(r'^penalty/list/all/$', views.penalty_list, name='penalty_list_all', kwargs={'show_all': True}),
    url(r'^penalty/new/$', views.penalty_new, name='penalty_new'),
    url(r'^penalty/(?P<pid>[0-9]+)/$', views.penalty_info, name='penalty_info'),
    url(r'^penalty/(?P<pid>[0-9]+)/edit/$', views.penalty_edit, name='penalty_edit'),
    url(r'^penalty/(?P<pid>[0-9]+)/delete/$', views.penalty_delete, name='penalty_delete'),

    url(r'^parking/list/$', views.parking_list, name='parking_list'),
    url(r'^parking/new/$', views.parking_new, name='parking_new'),
    url(r'^parking/(?P<pid>[0-9]+)/$', views.parking_info, name='parking_info'),
    url(r'^parking/(?P<pid>[0-9]+)/edit/$', views.parking_edit, name='parking_edit'),
    url(r'^parking/(?P<pid>[0-9]+)/delete/$', views.parking_delete, name='parking_delete'),

    url(r'^visitor/list/$', views.visitor_list, name='visitor_list'),
    url(r'^visitor/new/$', views.visitor_new, name='visitor_new'),
    url(r'^visitor/(?P<vid>[0-9]+)/$', views.visitor_info, name='visitor_info'),
    url(r'^visitor/(?P<vid>[0-9]+)/edit/$', views.visitor_edit, name='visitor_edit'),
    url(r'^visitor/(?P<vid>[0-9]+)/delete/$', views.visitor_delete, name='visitor_delete'),

    url(r'^reports/tracking/$', views.tracking_report_form, name='tracking_report_form'),
    url(r'^reports/tracking/web/$', views.tracking_report, name='tracking_report'),
    url(r'^reports/tracking/xls/$', views.tracking_report, name='tracking_report', kwargs={'xls': True}),

    url(r'^reports/general/$', views.general_report, name='general_report_web'),
    url(r'^reports/general/xls/$', views.general_report, name='general_report_xls', kwargs={'xls': True}),

    url(r'^reports/to/$', views.to_report_form, name='to_report_form'),
    url(r'^reports/to/web/$', views.to_report, name='to_report_web'),
    url(r'^reports/to/xls/$', views.to_report, name='to_report_xls', kwargs={'xls': True}),

    url(r'^reports/penalties/$', views.penalties_report_form, name='penalties_report_form'),
    url(r'^reports/penalties/web/$', views.penalties_report, name='penalties_report_web'),
    url(r'^reports/penalties/xls/$', views.penalties_report, name='penalties_report_xls', kwargs={'xls': True}),

    url(r'^reports/parking/$', views.parking_report, name='parking_report'),

    url(r'^reports/mileage/$', views.mileage_report_form, name='mileage_report_form'),
    url(r'^reports/mileage/web/$', views.mileage_report, name='mileage_report_web'),
    url(r'^reports/mileage/xls/$', views.mileage_report, name='mileage_report_xls', kwargs={'xls': True}),
]
