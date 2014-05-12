from django import forms
from django.forms import ModelForm
import floppyforms as forms2

from administrarItems.models import ItemBase, campoFile, campoEntero, campoImagen, campoTextoCorto, campoTextoLargo
from administrarTipoItem.models import TipoItem


class itemForm(forms.ModelForm):
    """
    Este es el formulario para la creacion de items
    """

    tipoitem = forms.ModelChoiceField(queryset=TipoItem.objects.all(), label='Tipo de Item')

    class Meta:
        model = ItemBase
        fields = ('nombre', 'complejidad', 'tiempo', 'costo', 'descripcion', 'tipoitem',)
        exclude = ( 'itemrelacion', )
        widgets = {
            'nombre': forms2.TextInput(attrs={'class': 'form-control', }),
            'complejidad': forms2.NumberInput(attrs={'class': 'form-control'}, ),
            'tiempo': forms2.NumberInput(attrs={'class': 'form-control', }),
            'costo': forms2.NumberInput(attrs={'class': 'form-control', }),
            'descripcion': forms2.Textarea(attrs={'class': 'form-control', }),

        }

    def __init__(self, *args, **kwargs):
        super(itemForm, self).__init__(*args, **kwargs)
        self.fields['tipoitem'].queryset = TipoItem.objects.all()

class campoEnteroForm(forms.ModelForm):
    """
    Este es el formulario para la creacion de campos enteros
    """
    class Meta:
        model = campoEntero
        fields = ('valor',)
        widgets = {
            'valor': forms2.NumberInput(attrs={'class': 'form-control', })
        }

    def __init__(self, *args, **kwargs):
        super(campoEnteroForm, self).__init__(*args, **kwargs)


class campoTextoCortoForm(forms.ModelForm):
    """
    Este es el formulario para la creacion de campos de texto cortos
    """
    class Meta:
        model = campoTextoCorto
        fields = ('valor',)
        widgets = {
            'valor': forms2.TextInput(attrs={'class': 'form-control', })
        }

    def __init__(self, *args, **kwargs):
        super(campoTextoCortoForm, self).__init__(*args, **kwargs)


class campoTextoLargoForm(forms.ModelForm):
    """
    Este es el formulario para la creacion de campos de texto largos
    """
    class Meta:
        model = campoTextoLargo
        fields = ('valor',)
        widgets = {
            'valor': forms2.TextInput(attrs={'class': 'form-control', })
        }

    def __init__(self, *args, **kwargs):
        super(campoTextoLargoForm, self).__init__(*args, **kwargs)


class campoFileForm(ModelForm):
    """
    Este es el formulario para la creacion de campos de texto largos
    """
    class Meta:
        model = campoFile
        fields = ('archivo',)


class campoImagenForm(ModelForm):
    """
    Este es el formulario para la creacion de campos de texto largos
    """
    class Meta:
        model = campoImagen
        fields = ('imagen',)

