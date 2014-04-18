"""
Descripcion de las diferentes URLs utilizadas en el proyecto ZAPpm
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from autenticacion.views import base, myLogin
from administrarUsuarios.views import createUser, changeUser, changePass
from administrarUsuarios.views import createUser, changeUser, userlist
from zar.views import about, contact

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', myLogin, {'template_name': 'autenticacion/login.html'}),
                       url(r'^login/$', myLogin, {'template_name': 'autenticacion/login.html'}),
                       url(r'^logout/$', logout_then_login, name="logout"),
                       url(r'^base/$', base, name="base"),
                       url(r'^about/$', about, name="about"),
                       url(r'^createuser/$', createUser),
                       url(r'^changeuser/$', changeUser),
                       url(r'^userlist/$', userlist, name="userlist"),
                       url(r'^changepass/$', changePass),
                       url(r'^contact/$', contact, name="contact"),
                       )