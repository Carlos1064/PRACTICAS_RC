from django import forms
from django.utils import timezone
from .models import Categoria, Oferta


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nombre', 'descripcion')
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 4})}


class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ('categoria', 'titulo', 'descripcion', 'requisitos', 'tipo', 'modalidad', 'vacantes', 'fecha_limite')
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5}),
            'requisitos': forms.Textarea(attrs={'rows': 4}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.order_by('nombre')

    def clean_fecha_limite(self):
        fecha = self.cleaned_data['fecha_limite']
        if fecha <= timezone.localdate():
            raise forms.ValidationError('La fecha límite debe ser posterior a hoy.')
        return fecha

    def clean_vacantes(self):
        vacantes = self.cleaned_data['vacantes']
        if vacantes < 1:
            raise forms.ValidationError('Debe existir al menos una vacante.')
        return vacantes
