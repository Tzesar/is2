"""
Descripcion de las diferentes URLs utilizadas en el proyecto ZAPpm
"""

from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from autenticacion.views import main, myLogin, UserResetPassword
from administrarUsuarios.views import createUser, changeUser, userList, changePass, changeAnyUser, changeUser2
from zar.views import about, contact
from administrarProyectos.views import createProject, changeProject, projectList, workProject, setUserToProject, viewSetUserProject
from administrarFases.views import changePhase, createPhase, phaseList, deletePhase
from administrarRolesPermisos.views import createRole, roleList, changeRole, deleteRole

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', myLogin, {'template_name': 'autenticacion/login.html'}),
                       url(r'^login/$', myLogin, {'template_name': 'autenticacion/login.html'}),
                       url(r'^logout/$', logout_then_login, name="logout"),
                       url(r'^main/$', main, name="main"),
                       url(r'^about/$', about, name="about"),
                       url(r'^createuser/$', createUser, name="createuser"),
                       url(r'^changeuser/$', changeUser, name="changeuser"),
                       url(r'^changeuser2/$', changeUser2, name="changeuser2"),
                       url(r'^changeanyuser/(?P<id_usuario>\d+)$', changeAnyUser, name="changeanyuser"),
                       url(r'^userlist/$', userList, name="userlist"),
                       url(r'^changepass/$', changePass, name="changepass"),
                       url(r'^contact/$', contact),
                       url(r'^createproject/$', createProject),
                       url(r'^changeproject/(?P<id_proyecto>\d+)$', changeProject, name='changeproject'),
                       url(r'^setusertoproject/(?P<id_proyecto>\d+)$', setUserToProject),
                       url(r'^usersetproject/(?P<id_proyecto>\d+)$', viewSetUserProject),
                       url(r'^projectlist/$', projectList, name='projectlist'),
                       url(r'^workproject/(?P<id_proyecto>\d+)$', workProject, name='workproject'),
                       url(r'^createphase/(?P<id_proyecto>\d+)$', createPhase),
                       url(r'^changephase/(?P<id_fase>\d+)$', changePhase),
                       url(r'^phaselist/(?P<id_proyecto>\d+)$', phaseList),
                       url(r'^deletephase/(?P<id_fase>\d+)$', deletePhase),
                       url(r'^createrole/(?P<id_proyecto>\d+)$', createRole),
                       url(r'^rolelist/(?P<id_proyecto>\d+)$', roleList, name="rolelist"),
                       url(r'^changerole/(?P<id_proyecto>\d+)/(?P<id_rol>\d+)$', changeRole, name="rolelist"),
                       url(r'^deleterole/(?P<id_proyecto>\d+)/(?P<id_rol>\d+)$', deleteRole),
                       url(r'^forgot_password/$', 'django.contrib.auth.views.password_reset', {'template_name':'autenticacion/forgot_password.html',\
                               'post_reset_redirect' : 'registration/password_reset_done'}, name="reset_password"),
                       url(r'^forgot_password/registration/password_reset_done/$', 'django.contrib.auth.views.password_reset_done'),
                       url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect': 'registration/password_reset_complete'}),
                       url(r'^/password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete'),
                       )

