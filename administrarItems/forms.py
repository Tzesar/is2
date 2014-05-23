#encoding:utf-8
from django import forms
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
import floppyforms as forms2

from administrarItems.models import ItemBase, CampoFile, CampoNumero, CampoImagen, CampoTextoCorto, CampoTextoLargo
from administrarTipoItem.models import TipoItem, Atributo


class itemForm(forms.ModelForm):
    """
    *Formulario para la creación de items, utilizamos el modelo* ``ItemBase``
        + *Nombre*: Nombre del Ítem
        + *Descripción*: Breve reseña del ítem
        + *Tipo de Ítem*: Tipo de ítem al cual pertenece el ítem.
        + *Complejidad*: Es el nivel complejidad que abarca el item.
        + *Costo*: Es el nivel costo de recurso estimados a utilizar para desarrollar el item.

    ::

        class Meta:
            model = ItemBase
            fields = ('nombre', 'complejidad', 'tiempo', 'costo', 'descripcion', 'tipoitem',)


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


class modificarDatosItemForm(forms.ModelForm):
    """
    * Formulario de modificacion de la configuracion general del item.*
    *Campos como el nombre del item, y su descripcion se incluyen en este formulario *

    ::

        class Meta:
            model = ItemBase
            fields = ('nombre', 'descripcion',)

    """
    class Meta:
        model = ItemBase
        fields = ('nombre', 'descripcion',)
        widgets = {
            'nombre': forms2.TextInput(attrs={'class': 'form-control', }),
            'descripcion': forms2.Textarea(attrs={'class': 'form-control', 'cols': 20, 'rows': 4, 'style': 'resize:none'})
        }


class modificarAtributosBasicosForm(forms.ModelForm):
    """
    *Formulario para modificar los atributos basicos de un item.*
    *Se incluyen en este formulario, los campos Complejidad, Costo y Tiempo.*
    ::

        class Meta:
            model = ItemBase
            fields = ('costo', 'complejidad', 'tiempo',)

    """
    class Meta:
        model = ItemBase
        fields = ('costo', 'complejidad', 'tiempo',)
        widgets = {
            'costo': forms2.NumberInput(attrs={'class': 'form-control',}),
            'complejidad': forms2.NumberInput(attrs={'class': 'form-control',}),
            'tiempo': forms2.NumberInput(attrs={'class': 'form-control',})
        }


#TODO: Eliminar si ya no se usa
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
            'valor': forms2.Textarea(attrs={'class': 'form-control', 'style': 'resize:none'})
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

    def __init__(self, *args, **kwargs):
        super(campoImagenForm, self).__init__(*args, **kwargs)
        self.fields['imagen'].required = False


class CustomInlineFormSet_NUM(BaseInlineFormSet):
    """
    *Formulario para los atributos del tipo numérico*
    """
    def __init__(self, *args, **kwargs):
        super(CustomInlineFormSet_NUM, self).__init__(*args, **kwargs)
        nro_formularios = len(self)

        item = ItemBase.objects.get(pk=self.instance.pk)
        atributosNumericos = Atributo.objects.filter(tipoDeItem=item.tipoitem, tipo='NUM')
        lista_campos_numericos = CampoNumero.objects.filter(item=item, atributo__in=atributosNumericos).order_by('id')

        for i in range(0, nro_formularios):
            self[i].fields['valor'].label = lista_campos_numericos[i].atributo.nombre


class CustomInlineFormSet_STR(BaseInlineFormSet):
    """
    *Formulario para los atributos del tipo alfanumérico*
    """
    def __init__(self, *args, **kwargs):
        super(CustomInlineFormSet_STR, self).__init__(*args, **kwargs)
        nro_formularios = len(self)

        item = ItemBase.objects.get(pk=self.instance.pk)
        atributosSTR = Atributo.objects.filter(tipoDeItem=item.tipoitem, tipo='STR')
        lista_campos_STR = CampoTextoCorto.objects.filter(item=item, atributo__in=atributosSTR).order_by('id')

        for i in range(0, nro_formularios):
            self[i].fields['valor'].label = lista_campos_STR[i].atributo.nombre


class CustomInlineFormSet_TXT(BaseInlineFormSet):
    """
    *Formulario para los atributos del tipo alfanumérico extendido*
    """
    def __init__(self, *args, **kwargs):
        super(CustomInlineFormSet_TXT, self).__init__(*args, **kwargs)
        nro_formularios = len(self)

        item = ItemBase.objects.get(pk=self.instance.pk)
        atributosTXT = Atributo.objects.filter(tipoDeItem=item.tipoitem, tipo='TXT')
        lista_campos_TXT = CampoTextoLargo.objects.filter(item=item, atributo__in=atributosTXT).order_by('id')

        for i in range(0, nro_formularios):
            self[i].fields['valor'].label = lista_campos_TXT[i].atributo.nombre


class CustomInlineFormSet_IMG(BaseInlineFormSet):
    """
    *Formulario para los atributos del tipo imagen*
    """
    def __init__(self, *args, **kwargs):
        super(CustomInlineFormSet_IMG, self).__init__(*args, **kwargs)
        nro_formularios = len(self)

        item = ItemBase.objects.get(pk=self.instance.pk)
        atributosIMG = Atributo.objects.filter(tipoDeItem=item.tipoitem, tipo='IMG')
        lista_campos_IMG = CampoImagen.objects.filter(item=item, atributo__in=atributosIMG).order_by('id')

        for i in range(0, nro_formularios):
            self[i].fields['imagen'].label = lista_campos_IMG[i].atributo.nombre


class CustomInlineFormSet_FIL(BaseInlineFormSet):
    """
    *Formulario para los atributos del tipo archivo*
    """
    def __init__(self, *args, **kwargs):
        super(CustomInlineFormSet_FIL, self).__init__(*args, **kwargs)
        nro_formularios = len(self)

        item = ItemBase.objects.get(pk=self.instance.pk)
        atributosFIL = Atributo.objects.filter(tipoDeItem=item.tipoitem, tipo='FIL')
        lista_campos_FIL = CampoFile.objects.filter(item=item, atributo__in=atributosFIL).order_by('id')

        for i in range(0, nro_formularios):
            self[i].fields['archivo'].label = lista_campos_FIL[i].atributo.nombre