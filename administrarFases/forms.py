#encoding=utf-8
from django.forms import ModelForm
from administrarFases.models import Fase
from django import forms
from administrarProyectos.models import Proyecto


class NewPhaseForm(forms.ModelForm):
    """
    Formulario para la creación de nuevas fases en el sistema.
    Opción válida solo para usuarios con roles correspondientes.

    Utilizamos el Modelo de Fase definido del cual filtramos los campos de tal manera a que solo se habiliten los
    campos necesarios para la creación de una fase en el proyecto.
    """

    class Meta:
        model = Fase
        fields = ('nombre', 'descripcion',)
        exclude = ('proyecto',)


class ChangePhaseForm(forms.ModelForm):
    """
    Formulario para la modificacion de proyectos creados en el sistema.

    Opción válida solo para usuarios con rol de Administrador.

    Utilizamos el Modelo de Fase definido del cual filtramos los campos de tal manera a que solo se habiliten los
    campos disponibles para la modificación de una fase en el proyecto.

    """

    class Meta:
        model = Fase
        fields = ('nombre', 'estado', 'descripcion',)

    def __init__(self, *args, **kwargs):
        super(ChangePhaseForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')