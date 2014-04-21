#encoding:utf-8
from __future__ import unicode_literals
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext, ugettext_lazy as _
from autenticacion.models import Usuario


class CustomUserCreationForm(forms.ModelForm):
    """
    Formulario para la creación de usuarios, especificar el nombre de usuario y la contraseña del nuevo usuario.

    Formulario para la creación usuarios por Django y personalizado para el proyecto ZARpm. Utiliza el modelo
    personalizado Usuario extendido del modelos User.

    Utilizamos el modelo Usuario del cual filtramos los campos de tal manera a que solo se habiliten los
    campos necesarios para la creación de un usuario en el sistema.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
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
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            Usuario._default_manager.get(username=username)
        except Usuario.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """
    Formulario para la modificacion de usuarios, donde se visualiza el formulario con los campos y opciones de modificacion disponibles

    Formulario para modificar usuarios propuesto por Django y personalizado para el proyecto ZARpm. Utiliza el modelo
    personalizado Usuario extendido del modelos User.

    Utilizamos el modelo Usuario, del cual filtramos los campos de tal manera a que solo se habiliten los
    campos disponibles para la modificación de un usuario en el sistema.

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


class CustomPasswordChangeForm(SetPasswordForm):
    """
    Formulario que permite a los usuarios cambiar la contraseña verificando con la contraseña anterior.
    Utiliza el modelo personalizado Usuario extendido del modelos User.

    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Verificacion de la contrasena anterior
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
