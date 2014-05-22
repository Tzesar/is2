#encoding:utf-8
from django import forms
import floppyforms as forms2
from administrarFases.models import Fase
from administrarItems.models import ItemBase
from administrarLineaBase.models import LineaBase, SolicitudCambios
from administrarProyectos.models import Proyecto
from administrarTipoItem.models import TipoItem


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


class createSCForm(forms.ModelForm):
    """
    Formulario para la creación de Solicitud de Cambios en el Sistema
    """
    class Meta:
        model = SolicitudCambios
        fields = ('motivo',)
        widgets = {
            'motivo': forms2.Textarea(attrs={'class': 'form-control', }),
        }

    def __init__(self, *args, **kwargs):
        super(createSCForm, self).__init__(*args, **kwargs)


class asignarItemSolicitudForm(forms2.Form):
    """
    *Formulario para vincular usuarios a un rol.
    *Establece las opciones a los usuarios vinculados al proyecto que estén **activos** y no sean el* **administrador**.

    :param id_proyecto: Argumento keyword que contiene el ``id`` del proyecto al cual se desea asignar a los usuarios.
    """

    items = forms2.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        id_fase = kwargs.pop('id_fase')
        self.fase = Fase.objects.get(id=id_fase)
        self.tipoitem = TipoItem.objects.filter(fase=self.fase)

        super(asignarItemSolicitudForm, self).__init__(*args, **kwargs)

        itemHabilitados = list(ItemBase.objects.filter(estado='ELB', tipoitem__in=self.tipoitem).order_by('nombre').values_list('id', 'nombre'))
        self.fields['items'] = forms2.MultipleChoiceField(choices=itemHabilitados, required=True,
                                                          widget=forms2.CheckboxSelectMultiple(attrs={'class': 'form-control', }), help_text='Items que serán modificados')

        super(asignarItemSolicitudForm, self).full_clean()


    def get_cleaned_data(self):
        """
        Retorna las opciones seleccionadas en la vista.
        :return: opciones: ``Lista`` de opciones del seleccionadas que existen dentro de las opciones iniciales del ``Form``.
        """

        opciones = self.cleaned_data.get('items')

        return opciones