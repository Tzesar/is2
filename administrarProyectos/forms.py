#encoding=utf-8
from django.forms import ModelForm
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
import floppyforms as forms2

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
    lider_proyecto = str(forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Usuario.objects.all(),
                                                label='Líder de Proyecto', required=True, ))


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


class ChangeProjectLeaderForm(forms2.ModelForm):
    """
    *Formulario para la modificación de proyectos creados en el sistema.  Utilizamos el modelo de* ``Proyecto``
    *definido del cual filtramos los campos de tal manera a que solo se habiliten los
    campos disponibles para la modificación de un proyecto en el sistema.*

    Opción válida solo para usuarios con rol de ``Lider``.

    :param args: Argumentos para el modelo base ``ModelForm``.
    :param kwargs: Keyword Arguments para la función ``ModelForm``.

    ::

        class Meta:
            model = Proyecto
            fields = ('nombre', 'lider_proyecto', 'estado', 'descripcion',)

    """

    class Meta:
        model = Proyecto
        fields = ('nombre', 'estado', 'fecha_inicio', 'fecha_fin', 'descripcion', 'observaciones')
        widgets = {
            'nombre': forms2.TextInput(attrs={'class': 'form-control', }),
            'estado': forms2.Select(attrs={'class': 'form-control', }),
            'fecha_inicio': forms2.DateInput(attrs={'class': 'form-control', }),
            'fecha_fin': forms2.DateInput(attrs={'class': 'form-control', }),
            'descripcion': forms2.Textarea(attrs={'class': 'form-control', }),
            'observaciones': forms2.Textarea(attrs={'class': 'form-control', }),
        }

    def __init__(self, *args, **kwargs):
        super(ChangeProjectLeaderForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

class setUserToProjectForm(forms2.Form):
    """
    *Formulario para vincular usuarios a un proyecto*

    :param args: Argumentos para el modelo base ``ModelForm``.
    :param kwargs: Keyword Arguments para el modelo ``ModelForm``.
    """

    usuarios = forms2.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        id_proyecto = kwargs.pop('id_proyecto')
        self.proyecto = Proyecto.objects.get(id=id_proyecto)
        super(setUserToProjectForm, self).__init__(*args, **kwargs)

        usuariosExcluidos = list(UsuariosVinculadosProyectos.objects.filter(cod_proyecto=self.proyecto).values_list('cod_usuario', flat=True))
        usuariosExcluidos.append(-1,)
        opciones = list(Usuario.objects.exclude(pk__in=usuariosExcluidos).filter(is_superuser=False, is_active=True).values_list('id', 'username'))

        self.fields['usuarios'].choices = opciones
        super(setUserToProjectForm, self).full_clean()

    def get_cleaned_data(self):
        """
        Retorna las opciones seleccionadas en la vista.
        :return: opciones: ``Lista`` de valores.
        """

        opciones = self.cleaned_data.get('usuarios')

        return opciones
