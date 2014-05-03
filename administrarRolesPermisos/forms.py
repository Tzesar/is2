#encoding=utf-8

from django import forms
import floppyforms as forms2

from administrarRolesPermisos.models import RolFase


class NewRoleForm(forms2.ModelForm):
    """
    Formulario para la creación de nuevos roles en un proyecto.
    Opción válida solo para usuarios con rol Líder de Proyecto.
    """

    permisos = forms.ModelMultipleChoiceField(queryset=RolFase.objects.all(), widget=forms2.CheckboxSelectMultiple, required=True)

    class Meta:
        model = RolFase
        fields = ('nombre', 'descripcion', 'permisos',)
        exclude = ('proyecto',)
        widgets = {
            'nombre': forms2.TextInput(attrs={'class': 'form-control', }),
            'descripcion': forms2.Textarea(attrs={'class': 'form-control', }),
        }


class ChangeRoleForm(forms2.ModelForm):
    """
    Formulario para la modificacion de proyectos creados en el sistema.
    Opción válida solo para usuarios con rol de Administrador.
    """

    permisos = forms.ModelMultipleChoiceField(queryset=RolFase.objects.all(), widget=forms2.CheckboxSelectMultiple, required=True)

    class Meta:
        model = RolFase
        fields = ('nombre', 'descripcion', 'permisos',)
        exclude = ('proyecto',)
        widgets = {
            'nombre': forms2.TextInput(attrs={'class': 'form-control', }),
            'descripcion': forms2.Textarea(attrs={'class': 'form-control', }),
        }


    def __init__(self, *args, **kwargs):
        super(ChangeRoleForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')


class AsignRoleForm(forms.ModelForm):

    roles_usuarios = forms.ModelMultipleChoiceField(queryset=RolFase.objects.none(), widget=forms.CheckboxSelectMultiple,
                                                    required=True, label='Usuarios del Proyecto')

    class Meta:
        model = RolFase
        fields = ('roles_usuarios',)