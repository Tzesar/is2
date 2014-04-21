#encoding=utf-8
from django.forms import ModelForm
from gestionRolesPermisos.models import RolFase
from django import forms


class NewRoleForm(ModelForm):
    """
    Formulario para la creación de nuevos roles en un proyecto.
    Opción válida solo para usuarios con rol Líder de Proyecto.
    """

    permisos = forms.ModelMultipleChoiceField(queryset=RolFase.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)

    class Meta:
        model = RolFase
        fields = ('nombre', 'descripcion', 'permisos',)
        exclude = ('proyecto',)



class ChangeRoleForm(forms.ModelForm):
    """
    Formulario para la modificacion de proyectos creados en el sistema.
    Opción válida solo para usuarios con rol de Administrador.
    """

    permisos = forms.ModelMultipleChoiceField(queryset=RolFase.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)

    class Meta:
        model = RolFase
        fields = ('nombre', 'descripcion', 'permisos',)


    def __init__(self, *args, **kwargs):
        super(ChangeRoleForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')