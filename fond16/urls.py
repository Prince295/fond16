"""fond16 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from app104.views import *
from django.contrib.auth import logout

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^fond16/login/$', authentificate_func),
    url(r'^fond16/profile/$', success_auth),
    url(r'^fond16/logout/$', logout_func),
    url(r'^load_cache/$', load_data, name='load_data'),
    url(r'^$', base, name='base'),
    url(r'^coord/$', coordination, name='coordination'),
    url(r'^coord/illness/$', Coordination_illness_views().view_empty_coordination_illness, name='coord_illness'),
    url(r'^coord/death/$', Coordination_death_views().view_empty_coordination_death, name='coord_death'),
    url(r'^load/$', onload, name='onload'),
    url(r'^mo_views/$', mo_views, name='mo_views'),
    url(r'^mo_views/table/$', mo_views_table, name='mo_views_table'),
    url(r'^mo_views/control_table/$', mo_views_ctrl_tbl, name='control_table'),
    url(r'^documents/$', documents_base, name='documents'),
    url(r'^documents/all/$', documents_all, name='docs_all'),
    url(r'^documents/new/$', documents_new, name='docs_new'),
    url(r'^coordination_death/(\w+)/$', Coordination_death_views().view_coordination_death, name='coord_death_tables'),
    url(r'^coordination_illness/(\w+)/$', Coordination_illness_views().view_coordination_illness, name='coord_illness_tables'),
    url(r'^coordination_illness_rebase/$', Coordination_illness_views().view_all_smo_class_names, name='coord_illness_rebase'),
    url(r'^return_classnames/$', Coordination_illness_views().view_coordination_illness_load_classes)
]
