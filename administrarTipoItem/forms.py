#encoding=utf-8
from django import forms
import floppyforms as forms2

from administrarTipoItem.models import TipoItem, Atributo


class NewItemTypeForm(forms.ModelForm):
    """
    *Formulario para la creación de tipos de ítems en el sistema.
    Opción válida solo para el usuario Líder de Proyecto.*

    :param args: Argumentos para el modelo base ``ModelForm``.
    :param kwargs: Keyword Arguments para la función ``ModelForm``.

    ::

            class Meta:
                model = TipoItem
                fields = ('nombre', 'descripcion',)
                exclude = ('fase',)

    """

    class Meta:
        model = TipoItem
        fields = ('nombre', 'descripcion',)
        exclude = ('fase',)
        widgets = {
            'nombre': forms2.TextInput(attrs={'class': 'form-control', }),
            'descripcion': forms2.TextInput(attrs={'class': 'form-control', }),
        }

    def __init__(self, *args, **kwargs):
        super(NewItemTypeForm, self).__init__(*args, **kwargs)


class ChangeItemTypeForm(forms.ModelForm):
    """
    *Formulario para la modificacion de tipos de ítems creados en el sistema.
    Opción válida solo para usuarios con rol de Administrador.*

    :param args: Argumentos para el modelo base ``ModelForm``.
    :param kwargs: Keyword Arguments para la función ``ModelForm``.

    ::

        class Meta:
            model = TipoItem
            fields = ('nombre', 'descripcion',)

    """

    class Meta:
        model = TipoItem
        fields = ('nombre', 'descripcion',)
        widgets = {
            'nombre': forms2.TextInput(attrs={'class': 'form-control', }),
            'descripcion': forms2.TextInput(attrs={'class': 'form-control', }),
        }

    def __init__(self, *args, **kwargs):
        super(ChangeItemTypeForm, self).__init__(*args, **kwargs)


class CreateAtributeForm(forms.ModelForm):
    """
    *Formulario para la creación de atributos del tipos de ítems en el sistema.
    Opción válida solo para el usuario Líder de Proyecto.*

    :param args: Argumentos para el modelo base ``ModelForm``.
    :param kwargs: Keyword Arguments para la función ``ModelForm``.

    """

    class Meta:
        model = Atributo
        fields = ('nombre', 'tipo', 'descripcion',)
        exclude = ('tipoDeItem',)
        widgets = {
            'nombre': forms2.TextInput(attrs={'class': 'form-control', }),
            'tipo': forms2.Select(attrs={'class': 'form-control', }),
            'descripcion': forms2.TextInput(attrs={'class': 'form-control', }),
        }

    def __init__(self, *args, **kwargs):
        super(CreateAtributeForm, self).__init__(*args, **kwargs)


class ChangeAtributeForm(forms.ModelForm):
    """
    *Formulario para la modificacion de tipos de ítems creados en el sistema.
    Opción válida solo para usuarios con rol de Administrador.*

    :param args: Argumentos para el modelo base ``ModelForm``.
    :param kwargs: Keyword Arguments para la función ``ModelForm``.

    ::

        class Meta:
            model = TipoItem
            fields = ('nombre', 'descripcion',)

    """

    class Meta:
        model = Atributo
        fields = ('nombre', 'tipo', 'descripcion',)
        widgets = {
            'nombre': forms2.TextInput(attrs={'class': 'form-control', }),
            'tipo': forms2.Select(attrs={'class': 'form-control', }),
            'descripcion': forms2.TextInput(attrs={'class': 'form-control', }),
        }

    def __init__(self, *args, **kwargs):
        super(ChangeAtributeForm, self).__init__(*args, **kwargs)