from django import forms
from .models import Postulacion


class MensajePostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ('mensaje',)
        widgets = {'mensaje': forms.Textarea(attrs={'rows': 4, 'maxlength': 1200, 'placeholder': 'Cuéntale brevemente a la empresa por qué te interesa esta oportunidad.'})}
        labels = {'mensaje': 'Mensaje para la empresa'}

    def clean_mensaje(self):
        return self.cleaned_data['mensaje'].strip()


class CambioEstadoForm(forms.Form):
    estado = forms.ChoiceField(label='Nuevo estado')

    def __init__(self, *args, postulacion, **kwargs):
        super().__init__(*args, **kwargs)
        self.postulacion = postulacion
        etiquetas = dict(Postulacion.Estado.choices)
        self.fields['estado'].choices = [(estado, etiquetas[estado]) for estado in postulacion.transiciones_disponibles]

    def clean_estado(self):
        estado = self.cleaned_data['estado']
        if estado not in self.postulacion.transiciones_disponibles:
            raise forms.ValidationError('Esta transición de estado no está permitida.')
        return estado
