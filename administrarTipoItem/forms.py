#encoding=utf-8
from django.forms import ModelForm
from administrarTipoItem.models import TipoItem, AtributosItem
from django import forms


class NewItemTypeForm(forms.ModelForm):
    """
    Formulario para la creación de tipos de ítems en el sistema.
    Opción válida solo para usuarios con roles correspondientes.
    """

    class Meta:
        model = TipoItem
        fields = ('nombre', )
        exclude = ('perteneFase',)


class ChangeItemTypeForm(forms.ModelForm):
    """
    Formulario para la modificacion de tipos de ítems creados en el sistema.
    Opción válida solo para usuarios con rol de Administrador.
    """

    class Meta:
        model = TipoItem
        fields = ('nombre',)

    def __init__(self, *args, **kwargs):
        super(ChangeItemTypeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')