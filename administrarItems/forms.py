from django import forms
from django.forms import ModelForm
import floppyforms as forms2

from administrarItems.models import ItemBase, CampoFile, CampoNumero, CampoImagen, CampoTextoCorto, CampoTextoLargo
from administrarTipoItem.models import TipoItem


class itemForm(forms.ModelForm):
    """
    Este es el formulario para la creacion de items
    """

    tipoitem = forms.ModelChoiceField(queryset=TipoItem.objects.all(), label='Tipo de Item')

    class Meta:
        model = ItemBase
        fields = ('nombre', 'complejidad', 'tiempo', 'costo', 'descripcion', 'tipoitem',)
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
        model = CampoNumero
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
        model = CampoTextoCorto
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
        model = CampoTextoLargo
        fields = ('valor',)
        widgets = {
            'valor': forms2.TextInput(attrs={'class': 'form-control', })
        }

    def __init__(self, *args, **kwargs):
        super(campoTextoLargoForm, self).__init__(*args, **kwargs)


class campoFileForm(forms.ModelForm):
    """
    Este es el formulario para la creacion de campos de texto largos
    """
    class Meta:
        model = CampoFile
        fields = ('archivo',)

    def __init__(self, *args, **kwargs):
        super(campoFileForm, self).__init__(*args, **kwargs)
        self.fields['archivo'].required = False


class campoImagenForm(forms.ModelForm):
    class Meta:
        model = CampoImagen
        fields = ('imagen',)
