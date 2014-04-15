from django.forms import ModelForm
from django import forms
from autenticacion.models import Usuario


class NewProyectoForm(forms.Form):
    nombre = forms.CharField(label='Nombre del Proyecto')
    lider_proyecto = forms.CharField(label='Usuario responsable del proyecto')
    descripcion = forms.CharField(widget=forms.Textarea)
    fecha_inicio = forms.DateField(label='Fecha de Inicio del Proyecto')
    fecha_fin = forms.DateField(label='Fecha estimada de Finalización')



