"""
Descripcion de las diferentes URLs utilizadas en el proyecto ZAPpm
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from autenticacion.views import base, myLogin
from administrarUsuarios.views import createUser, changeUser, userList, changePass, changeAnyUser
from zar.views import about, contact
from administrarProyectos.views import createProject, changeProject, projectlist, setUserToProject, viewSetUserProject
from administrarFases.views import changePhase, createPhase, phaseList, deletePhase

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
                       url(r'^changeanyuser/(?P<id_usuario>\d+)$', changeAnyUser),
                       url(r'^userlist/$', userList, name="userlist"),
                       url(r'^changepass/$', changePass),
                       url(r'^contact/$', contact, name="contact"),
                       url(r'^createproject/$', createProject),
                       url(r'^changeproject/(?P<id_proyecto>\d+)$', changeProject),
                       url(r'^setusertoprojec/(?P<id_proyecto>\d+)$', setUserToProject),
                       url(r'^usersetproject/(?P<id_proyecto>\d+)$', viewSetUserProject),
                       url(r'^projectlist/$', projectlist),
                       url(r'^createphase/(?P<id_proyecto>\d+)$', createPhase),
                       url(r'^changephase/(?P<id_fase>\d+)$', changePhase),
                       url(r'^phaselist/(?P<id_proyecto>\d+)$', phaseList),
                       url(r'^deletephase/(?P<id_fase>\d+)$', deletePhase),
                       )