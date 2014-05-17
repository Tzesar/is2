#encoding=utf-8

from django import forms
from guardian.forms import BaseObjectPermissionsForm
from django.contrib.auth.models import Permission
from django.contrib.auth.models import ContentType
from guardian.shortcuts import assign_perm
from guardian.shortcuts import remove_perm
from guardian.shortcuts import get_perms
import floppyforms as forms2

from administrarProyectos.models import UsuariosVinculadosProyectos, Proyecto
from administrarRolesPermisos.models import Rol
from autenticacion.models import Usuario


class myBaseObjectPermissionsForm(BaseObjectPermissionsForm):
    """
    Redefinición de la clase ``BaseObjectPermissionsForm`` para cambiar el nombre del campo que se va a modificar
    para permitir varias renderizaciones en el mismo template.
    """

    def __init__(self, obj, *args, **kwargs):
        """
        :param obj: Any instance which form would use to manage object
          permissions"
        """
        self.obj = obj
        self.field_name = kwargs.pop('field_name', 'permisos')
        self.field_label = kwargs.pop('field_label', 'Permisos')
        self.attrs = kwargs.pop('attrs', None)
        super(myBaseObjectPermissionsForm, self).__init__(obj, *args, **kwargs)
        field_name = self.get_obj_perms_field_name()
        self.fields[field_name] = self.get_obj_perms_field()


    def get_obj_perms_field_name(self):
        """
        Returns name of the object permissions management field. Default:
        ``permission``.
        """

        return str(self.field_name)

    def get_obj_perms_field_label(self):
        """
        Returns label of the object permissions management field. Defualt:
        ``_("Permissions")`` (marked to be translated).
        """
        return str(self.field_label)

    def get_obj_perms_field_choices(self):
        """
        *Retorna la lista de ``Permisos`` disponibles sobre el objeto.*
        *La lista de opciones ``choices`` se obtiene hallando el ``contentType`` del objeto, *
        *luego se accede a los ``Permisos`` y se crea una lista, donde cada elemento tiene dos valores, *
        *el ``codename`` y el ``name`` de cada ``Permiso``.*
        *Por último, se obvian los primeros tres permisos, reservados solo para los usuarios ``Líder`` y *
        *``Administrador``,  que son ``Crear...``, ``Modificar...`` y ``Eliminar``.*
        """

        # Se crea una lista con los tipos de modelos que se pueden modificar (fase, proyecto, tipo de item, item, rol).
        # Luego se obtienen los permisos disponibles sobre esos modelos, excluyendo los permisos que crea django (crear,
        #   modificar y borrar).
        # Por ultimo se crea una lista asociando cada conjunto de permisos de cada modelo en una lista.

        contentType = ContentType.objects.get_for_model(self.obj)
        permisos = []
        perm = Permission.objects.filter(content_type_id=contentType).order_by('id').values_list('codename', 'name')
        permSliced = perm[3:]
        if permSliced:
            permisos.extend(permSliced)

        choices = permisos
        return choices


class RoleObjectPermissionsForm(myBaseObjectPermissionsForm):
    """
    Re-implementacion de la clase ``RoleObjectPermissionsForm`` para permitir varias renderizaciones
    en el mismo template.
    """

    def __init__(self, group, *args, **kwargs):
        self.group = group
        super(RoleObjectPermissionsForm, self).__init__(*args, **kwargs)

    def get_obj_perms_field_initial(self):
        perms = get_perms(self.group, self.obj)
        return perms

    def get_obj_perms_field_widget(self):
        """
        *Retorna el widget del campo que maneja los permisos por objeto.
        Además, establece atributos HTML al widget.*

        :param self.attrs: Un diccionario con los atributos HTML que se asignarán al widget.
        :return: El tipo ``field.SelectMultiple`` con los atributos establecidos.
        """

        if self.attrs:
            return forms.SelectMultiple(attrs=self.attrs)

        return forms.SelectMultiple(attrs={'class': 'form-control'})

    def save_obj_perms(self):
        """
        *Guarda los permisos seleccionados sobre el objeto creando nuevos y removiendo aquellos que ya no estén seleccionados*
        * pero ya existen.*

        *Este método debe ser llamado **luego** de que el ``Form`` sea validado.*
        """
        perms = self.cleaned_data[self.get_obj_perms_field_name()]
        model_perms = [c[0] for c in self.get_obj_perms_field_choices()]

        to_remove = set(model_perms) - set(perms)
        for perm in to_remove:
            remove_perm(perm, self.group, self.obj)

        for perm in perms:
            assign_perm(perm, self.group, self.obj)


class NuevoRolForm(forms2.ModelForm):
    """
    *Formulario para la creacion de nuevos roles del tipo ``Rol`` dentro de un proyecto*
    """

    class Meta:
        model = Rol
        fields = ('name', )
        exclude = ('permissions', 'objects', 'proyecto')
        widgets = {
            'name': forms2.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(NuevoRolForm, self).__init__(*args, **kwargs)

class asignarUsuariosRolForm(forms2.Form):
    """
    *Formulario para vincular usuarios a un rol.
    *Establece las opciones a los usuarios vinculados al proyecto que estén **activos** y no sean el* **administrador**.

    :param id_proyecto: Argumento keyword que contiene el ``id`` del proyecto al cual se desea asignar a los usuarios.
    """

    usuarios = forms2.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        id_proyecto = kwargs.pop('id_proyecto')
        self.proyecto = Proyecto.objects.get(id=id_proyecto)
        super(asignarUsuariosRolForm, self).__init__(*args, **kwargs)

        usuariosHabilitados = list(UsuariosVinculadosProyectos.objects.filter(cod_proyecto=self.proyecto.id, habilitado=True).values_list('cod_usuario', flat=True))
        opciones = list(Usuario.objects.filter(pk__in=usuariosHabilitados).values_list('id', 'username'))
        self.fields['usuarios'] = forms2.MultipleChoiceField(choices=opciones)

        super(asignarUsuariosRolForm, self).full_clean()

    def get_cleaned_data(self):
        """
        Retorna las opciones seleccionadas en la vista.
        :return: opciones: ``Lista`` de opciones del seleccionadas que existen dentro de las opciones iniciales del ``Form``.
        """

        opciones = self.cleaned_data.get('usuarios')

        return opciones