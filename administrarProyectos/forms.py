#encoding=utf-8
from django.forms import ModelForm
from django import forms

from administrarProyectos.models import Proyecto, UsuariosVinculadosProyectos

from autenticacion.models import Usuario


class NewProjectForm(ModelForm):
    """
    *Formulario para la creación de nuevos proyectos en el sistema. Utilizamos el modelo de* ``Proyecto``
    *definido del cual filtramos los campos de tal manera a que solo se habiliten los
    campos necesarios para la creación de un proyecto en el sistema.*

    Opción válida solo para usuarios con rol de ``Administrador``.

    :param args: Argumentos para el modelo base ``ModelForm``.
    :param kwargs: Keyword Arguments para la función ``ModelForm``.

    ::

        class Meta:
            model = Proyecto
            fields = ('nombre', 'lider_proyecto', 'descripcion',)

    """

    class Meta:
        model = Proyecto
        fields = ('nombre', 'lider_proyecto', 'descripcion',)


    def __init__(self, *args, **kwargs):
        super(NewProjectForm, self).__init__(*args, **kwargs)


class ChangeProjectForm(forms.ModelForm):
    """
    *Formulario para la modificación de proyectos creados en el sistema.  Utilizamos el modelo de* ``Proyecto``
    *definido del cual filtramos los campos de tal manera a que solo se habiliten los
    campos disponibles para la modificación de un proyecto en el sistema.*

    Opción válida solo para usuarios con rol de ``Administrador``.

    :param args: Argumentos para el modelo base ``ModelForm``.
    :param kwargs: Keyword Arguments para la función ``ModelForm``.

    ::

        class Meta:
            model = Proyecto
            fields = ('nombre', 'lider_proyecto', 'estado', 'descripcion',)

    """

    class Meta:
        model = Proyecto
        fields = ('nombre', 'lider_proyecto', 'estado', 'descripcion',)

    def __init__(self, *args, **kwargs):
        super(ChangeProjectForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')


class setUserToProjectForm(forms.ModelForm):
    """
    *Formulario para vincular usuarios a un proyecto*

    :param args: Argumentos para el modelo base ``ModelForm``.
    :param kwargs: Keyword Arguments para el modelo ``ModelForm``.
    """
    user = Usuario.objects.all()
    cod_usuario = str(forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple, queryset=user,
                                         label='Usuarios Vinculados', required=True, ))

    class Meta:
        model = UsuariosVinculadosProyectos
        fields = ('cod_usuario',)

    def __init__(self, *args, **kwargs):
        super(setUserToProjectForm, self).__init__(*args, **kwargs)