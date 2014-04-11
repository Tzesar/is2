from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from autenticacion.views import base, myLogin
from administrarUsuarios.views import createUser, changeUser
from zar.views import about

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', myLogin, {'template_name': 'autenticacion/login.html'}),
                       url(r'^login/$', myLogin, {'template_name': 'autenticacion/login.html'}),
                       url(r'^logout/$', logout_then_login, name="logout"),
                       url(r'^base/$', base, name="base"),
                       url(r'^about/$', about, name="about"),
                       url(r'^createuser/$', createUser),
                       url(r'^changeuser/$', changeUser)
                       )