"""aho URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urls_main = [
    url(r'^$', views.index, name='index'),

    url(r'^dvsync/$', views.dv_sync, name='dvsync'),

    url(r'^department/list/$', views.department_list, name='department_list'),
    url(r'^department/new/$', views.department_new, name='department_new'),
    url(r'^department/(?P<did>[0-9]+)/$', views.department_info, name='department_info'),
    url(r'^department/(?P<did>[0-9]+)/edit/$', views.department_edit, name='department_edit'),
    url(r'^department/(?P<did>[0-9]+)/delete/$', views.department_delete, name='department_delete'),

    url(r'^employee/list/$', views.employee_list, name='employee_list'),
    url(r'^employee/new/$', views.employee_new, name='employee_new'),
    url(r'^employee/(?P<eid>[0-9]+)/$', views.employee_info, name='employee_info'),
    url(r'^employee/(?P<eid>[0-9]+)/edit/$', views.employee_edit, name='employee_edit'),
    url(r'^employee/(?P<eid>[0-9]+)/delete/$', views.employee_delete, name='employee_delete'),

    url(r'^contact/list/$', views.contact_list, name='contact_list'),
    url(r'^contact/new/$', views.contact_new, name='contact_new'),
    url(r'^contact/(?P<uid>[0-9]+)/$', views.contact_info, name='contact_info'),
    url(r'^contact/(?P<uid>[0-9]+)/edit/$', views.contact_edit, name='contact_edit'),
]

urlpatterns = [
    url(r'^aho/keep_session$', views.keep_session, name='keep_session'),
    url(r'^aho/admin/', admin.site.urls),
    url(r'^aho/', include(urls_main, namespace='main', app_name='main')),
    url(r'^aho/aho/', include('aho.urls')),
    url(r'^aho/td/', include('td.urls')),
    url(r'^aho/mobile/', include('mobile.urls')),
    url(r'^aho/service/', include('service.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
