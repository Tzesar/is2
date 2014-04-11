from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
from autenticacion.views import base
from administrarUsuarios.views import createuser

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^login/$', login, {'template_name': 'autenticacion/login.html'}),
                       url(r'^logout/$', logout_then_login, name="logout"),
                       url(r'^base/$', base, name="base"),
                       url(r'^createuser/$', createuser),  )