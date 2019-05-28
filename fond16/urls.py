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

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', load_data, name='load_data'),
    url(r'^base/$', base, name='base'),
    url(r'^coord/$', coordination, name='coordination'),
    url(r'^coord/illness/$', coord_illness, name='coord_illness'),
    url(r'^coord/death/$', coord_death, name='coord_death'),
    url(r'^load/$', onload, name='onload'),
    url(r'^mo_views/$', mo_views, name='mo_views'),
    url(r'^mo_views/table/$', mo_views_table, name='mo_views_table'),
    url(r'^mo_views/control_table/$', mo_views_ctrl_tbl, name='control_table'),
    url(r'^documents/$', documents_base, name='documents'),
    url(r'^documents/all/$', documents_all, name='docs_all'),
    url(r'^documents/new/$', documents_new, name='docs_new')
]
