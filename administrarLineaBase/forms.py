#encoding:utf-8
from django import forms
import floppyforms as forms2
from administrarLineaBase.models import LineaBase


class createLBForm(forms.ModelForm):
    """
    Formulario para la creación de líneas base
    """
    class Meta:
        model = LineaBase
        fields = ('observaciones',)
        widgets = {
            'observaciones': forms2.Textarea(attrs={'class': 'form-control', }),
        }
