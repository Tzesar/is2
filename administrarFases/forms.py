#encoding=utf-8
from django import forms

from administrarFases.models import Fase


class NewPhaseForm(forms.ModelForm):
    """
    *Formulario para la creación de nuevas fases en el sistema. Utilizamos el modelo de ``Fase`` definido,
    del cual filtramos los campos de tal manera a que solo se habiliten los
    campos necesarios para la creación de una fase en el proyecto.
    Opción válida solo para usuarios con roles correspondientes.* 

    ::

        class Meta:
        model = Fase
        fields = ('nombre', 'descripcion',)
        exclude = ('proyecto',)

    """

    class Meta:
        model = Fase
        fields = ('nombre', 'descripcion',)
        exclude = ('proyecto',)

    def __init__(self, *args, **kwargs):
        super(NewPhaseForm, self).__init__(*args, **kwargs)

class ChangePhaseForm(forms.ModelForm):
    """
    *Formulario para la modificacion de proyectos creados en el sistema. Utilizamos el modelo de ``Fase``
    definido del cual filtramos los campos de tal manera a que solo se habiliten los
    campos disponibles para la modificación de una fase en el proyecto.*

    *Opción válida solo para usuarios con los roles correspondientes.*

    ::

        class Meta:
            model = Fase
            fields = ('nombre', 'estado', 'descripcion',)

    """

    class Meta:
        model = Fase
        fields = ('nombre', 'estado', 'descripcion',)

    def __init__(self, *args, **kwargs):
        super(ChangePhaseForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')