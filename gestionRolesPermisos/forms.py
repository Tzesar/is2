#encoding=utf-8
from django.forms import ModelForm
from gestionRolesPermisos.models import Rol
from django import forms


class NewRoleForm(ModelForm):
    """
    Formulario para la creación de nuevos roles en un proyecto.
    Opción válida solo para usuarios con rol Líder de Proyecto.
    """
    class Meta:
        model = Rol
        fields = ('nombre', 'descripcion', 'permisos',)
