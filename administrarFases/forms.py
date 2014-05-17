#encoding=utf-8

import floppyforms as forms2

from administrarFases.models import Fase


class NewPhaseForm(forms2.ModelForm):
    """
    *Formulario para la creación de nuevas fases en el sistema. Utilizamos el modelo de* ``Fase``
    *definido,del cual filtramos los campos de tal manera a que solo se habiliten los *
    *campos necesarios para la creación de una fase en el proyecto.*
    *Opción válida solo para usuarios con roles correspondientes.*

    :param args: Argumentos para el modelo ``ModelForm``.
    :param kwargs: Keyword Arguments para la el modelo ``ModelForm``.

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
        widgets = {
            'nombre': forms2.TextInput(attrs={'class': 'form-control', }),
            'descripcion': forms2.Textarea(attrs={'class': 'form-control', }),
        }

    def __init__(self, *args, **kwargs):
        super(NewPhaseForm, self).__init__(*args, **kwargs)


class ChangePhaseForm(forms2.ModelForm):
    """
    *Formulario para la modificacion de proyectos creados en el sistema. Utilizamos el modelo de* ``Fase``
    *definido del cual filtramos los campos de tal manera a que solo se habiliten los*
    *campos disponibles para la modificación de una fase en el proyecto.*

    *Opción válida solo para usuarios con los roles correspondientes.*

    :param args: Argumentos para el modelo ``ModelForm``.
    :param kwargs: Keyword Arguments para la el modelo ``ModelForm``.

    ::

        class Meta:
            model = Fase
            fields = ('nombre', 'descripcion',)

    """

    class Meta:
        model = Fase
        fields = ('nombre', 'descripcion',)
        widgets = {
            'nombre': forms2.TextInput(attrs={'class': 'form-control', }),
            'descripcion': forms2.Textarea(attrs={'class': 'form-control', }),
        }

    def __init__(self, *args, **kwargs):
        super(ChangePhaseForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')