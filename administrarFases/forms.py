#encoding=utf-8
from django.forms import ModelForm
from administrarFases.models import Fases
from django import forms


class NewPhaseForm(ModelForm):
    """
    Formulario para la creación de nuevas fases en el sistema.
    Opción válida solo para usuarios con roles correspondientes.
    """
    class Meta:
        model = Fases
        fields = ('nombre', 'descripcion',)


class ChangePhaseForm(forms.ModelForm):
    """
    Formulario para la modificacion de proyectos creados en el sistema.
    Opción válida solo para usuarios con rol de Administrador.
    """
    class Meta:
        model = Fases
        fields = ('nombre', 'estado', 'descripcion',)

    def __init__(self, *args, **kwargs):
        super(ChangePhaseForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')