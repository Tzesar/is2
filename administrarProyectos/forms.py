#encoding=utf-8
from django.forms import ModelForm
from django import forms

from administrarProyectos.models import Proyecto, UsuariosVinculadosProyectos

from autenticacion.models import Usuario


class NewProjectForm(ModelForm):
    """
    Formulario para la creación de nuevos proyectos en el sistema.

    Opción válida solo para usuarios con rol de Administrador.

    Utilizamos el Modelo de Proyecto definido del cual filtramos los campos de tal manera a que solo se habiliten los
    campos necesarios para la creación de un proyecto en el sistema.
    """

    class Meta:
        model = Proyecto
        fields = ('nombre', 'lider_proyecto', 'descripcion',)


class ChangeProjectForm(forms.ModelForm):
    """
    Formulario para la modificacion de proyectos creados en el sistema.

    Opción válida solo para usuarios con rol de Administrador.

    Utilizamos el Modelo de Proyecto definido del cual filtramos los campos de tal manera a que solo se habiliten los
    campos disponibles para la modificación de un proyecto en el sistema.
    """

    class Meta:
        model = Proyecto
        fields = ('nombre', 'lider_proyecto', 'estado', 'descripcion',)

    def __init__(self, *args, **kwargs):
        super(ChangeProjectForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')


class addUserProjectForm(forms.ModelForm):
    """
    Formulario para vincular usuarios a un proyecto
    """
    user = Usuario.objects.all()
    usuarios_asociados = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                        queryset=user, label='Usuarios Vinculados', required=True, )

    class Meta:
        model = Proyecto
        fields = ('usuarios_asociados',)


class setUserToProject(forms.ModelForm):
    """
    Formulario para vincular usuarios a un proyecto
    """
    user = Usuario.objects.all()
    cod_usuario = str(forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple, queryset=user,
                                         label='Usuarios Vinculados', required=True, ))

    class Meta:
        model = UsuariosVinculadosProyectos
        fields = ('cod_usuario',)