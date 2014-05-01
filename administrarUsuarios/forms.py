#encoding:utf-8
from __future__ import unicode_literals
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms2
from autenticacion.models import Usuario


class CustomUserCreationForm(forms.ModelForm):
    """
    *Formulario para la creación de usuarios.Utilizamos el modelo* ``Usuario`` del cual filtramos los campos de tal manera a que solo se habiliten los
    campos necesarios para la creación de un usuario en el sistema.
    Formulario para la creación usuarios por Django y personalizado para el proyecto ZARpm. Utiliza el modelo
    personalizado Usuario extendido del modelos User.

    :param args: Argumentos para el modelo ``ModelForm``.
    :param kwargs: Keyword Arguments para el modelo ``ModelForm``.

    ::

        class Meta:
            model = Usuario
            fields = ("username",)

    """
    error_messages = {
        'duplicate_username': ("Ya existe un usuario con el nombre de usuario especificado."),
        'password_mismatch': ("Las contraseñas no coinciden."),
    }

    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput)

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = Usuario
        fields = ("username",)

    def clean_username(self):
        """
        *Función responsable de validar la unicidad del nombre de usuario dentro del sistema. Si existe error no se
        creará el usuario.*
        """
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            Usuario._default_manager.get(username=username)
        except Usuario.DoesNotExist:
            return username
        print self.error_messages['duplicate_username']
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        """
        *Función responsable de confirmar la contraseña ingresada por el usuario, de tal manera que las contraseñas
        coincidan.* ``Contraseña1 == Contraseña2``
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            print self.error_messages['password_mismatch']
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch', )
        return password2

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)


class CustomUserChangeForm(forms.ModelForm):
    """
    *Formulario para la modificacion de usuarios. Utilizamos el modelo* ``Usuario``, *del cual filtramos los campos de tal manera a que solo se habiliten los
    campos disponibles para la modificación de un usuario en el sistema.
    Formulario para modificar usuarios propuesto por Django y personalizado para el proyecto ZARpm. Utiliza el modelo
    personalizado Usuario extendido del modelos User.*

    :param args: Argumentos para el modelo ``ModelForm``.
    :param kwargs: Keyword Arguments para el modelo ``ModelForm``.

    ::

        class Meta:
            model = Usuario
            fields = ('first_name', 'last_name', 'email', 'telefono',)
            exclude = ('username', 'password',)


    """

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'telefono',)
        exclude = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CambiarUsuarioForm(forms2.ModelForm):
    """
    *Formulario para la modificacion de usuarios. Utilizamos el modelo* ``Usuario``, *del cual filtramos los campos de tal manera a que solo se habiliten los
    campos disponibles para la modificación de un usuario en el sistema./n
    Formulario para modificar usuarios propuesto por Django y personalizado para el proyecto ZARpm. Utiliza el modelo
    personalizado Usuario extendido del modelo User.*

    :param args: Argumentos para el modelo ``ModelForm``.
    :param kwargs: Keyword Arguments para el modelo ``ModelForm``.

    ::

        class Meta:
            model = Usuario
            fields = ('first_name', 'last_name', 'email', 'telefono',)
            exclude = ('username', 'password',)

    """

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'telefono',)
        exclude = ('username', 'password',)
        widgets = {
            'first_name': forms2.TextInput(attrs={'class': 'form-control', }),
            'last_name': forms2.TextInput(attrs={'class': 'form-control', }),
            'email': forms2.EmailInput(attrs={'class': 'form-control', }),
            'telefono': forms2.TextInput(attrs={'class': 'form-control', }),
        }

    def __init__(self, *args, **kwargs):
        super(CambiarUsuarioForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

class CustomPasswordChangeForm(SetPasswordForm):
    """
    *Formulario que permite a los usuarios cambiar la contraseña confirmando con la contraseña anterior.
    Utiliza el modelo personalizado*  ``Usuario``.

    :param args: Argumentos para el modelo ``SetPasswordForm``.
    :param kwargs: Keyword Arguments para el modelo ``SetPasswordForm``.

    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')


    def clean_old_password(self):
        """
        *Funcion que confirma la contrasena anterior ingresada por el usuario. Si las contraseñas no coinciden no
        se realizará ningún cambio en la contraseña.*
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

CustomPasswordChangeForm_fields = SortedDict([
    (k, CustomPasswordChangeForm.base_fields[k])
        for k in ['old_password', 'new_password1', 'new_password2']])



