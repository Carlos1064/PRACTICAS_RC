from django import forms
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Empresa, PerfilEstudiante, Usuario


class RegistroEstudianteForm(forms.Form):
    nombre = forms.CharField(label='Nombre completo', max_length=150)
    correo = forms.EmailField(label='Correo electrónico')
    programa = forms.CharField(label='Programa académico', max_length=150)
    semestre = forms.IntegerField(label='Semestre', min_value=1, max_value=20, required=False)
    ciudad = forms.CharField(label='Ciudad', max_length=100)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, strip=False)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, strip=False)

    def clean_correo(self):
        correo = self.cleaned_data['correo'].strip().lower()
        if Usuario.objects.filter(correo__iexact=correo).exists():
            raise ValidationError('Ya existe una cuenta con este correo electrónico.')
        return correo

    def clean(self):
        datos = super().clean()
        if datos.get('password1') and datos.get('password2') and datos['password1'] != datos['password2']:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        if datos.get('password1'):
            usuario = Usuario(nombre=datos.get('nombre', ''), correo=datos.get('correo', ''))
            try:
                password_validation.validate_password(datos['password1'], usuario)
            except ValidationError as error:
                self.add_error('password1', error)
        return datos

    @transaction.atomic
    def save(self):
        usuario = Usuario.objects.create_user(
            correo=self.cleaned_data['correo'],
            password=self.cleaned_data['password1'],
            nombre=self.cleaned_data['nombre'],
            rol=Usuario.Rol.ESTUDIANTE,
        )
        PerfilEstudiante.objects.create(
            usuario=usuario,
            programa=self.cleaned_data['programa'],
            semestre=self.cleaned_data.get('semestre'),
            ciudad=self.cleaned_data['ciudad'],
        )
        return usuario


class RegistroEmpresaForm(forms.Form):
    nombre = forms.CharField(label='Nombre de quien representa a la empresa', max_length=150)
    correo = forms.EmailField(label='Correo electrónico')
    razon_social = forms.CharField(label='Razón social', max_length=180)
    nit = forms.CharField(label='NIT', max_length=30)
    sector = forms.CharField(label='Sector', max_length=100)
    ciudad = forms.CharField(label='Ciudad', max_length=100)
    descripcion = forms.CharField(label='Descripción de la empresa', widget=forms.Textarea)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, strip=False)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, strip=False)

    def clean_correo(self):
        correo = self.cleaned_data['correo'].strip().lower()
        if Usuario.objects.filter(correo__iexact=correo).exists():
            raise ValidationError('Ya existe una cuenta con este correo electrónico.')
        return correo

    def clean_nit(self):
        nit = self.cleaned_data['nit'].strip()
        if Empresa.objects.filter(nit__iexact=nit).exists():
            raise ValidationError('Ya existe una empresa registrada con este NIT.')
        return nit

    def clean(self):
        datos = super().clean()
        if datos.get('password1') and datos.get('password2') and datos['password1'] != datos['password2']:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        if datos.get('password1'):
            usuario = Usuario(nombre=datos.get('nombre', ''), correo=datos.get('correo', ''))
            try:
                password_validation.validate_password(datos['password1'], usuario)
            except ValidationError as error:
                self.add_error('password1', error)
        return datos

    @transaction.atomic
    def save(self):
        usuario = Usuario.objects.create_user(
            correo=self.cleaned_data['correo'],
            password=self.cleaned_data['password1'],
            nombre=self.cleaned_data['nombre'],
            rol=Usuario.Rol.EMPRESA,
        )
        Empresa.objects.create(
            usuario=usuario,
            razon_social=self.cleaned_data['razon_social'],
            nit=self.cleaned_data['nit'],
            sector=self.cleaned_data['sector'],
            ciudad=self.cleaned_data['ciudad'],
            descripcion=self.cleaned_data['descripcion'],
            estado=Empresa.Estado.PENDIENTE,
        )
        return usuario


class IngresoForm(AuthenticationForm):
    username = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    password = forms.CharField(label='Contraseña', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

    error_messages = {
        'invalid_login': 'El correo o la contraseña no son correctos.',
        'inactive': 'Esta cuenta está desactivada. Contacta al administrador.',
    }
