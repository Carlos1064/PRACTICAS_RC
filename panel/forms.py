from django import forms
from ofertas.models import Categoria


class ReporteFiltrosForm(forms.Form):
    desde = forms.DateField(label='Desde', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    hasta = forms.DateField(label='Hasta', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    categoria = forms.ModelChoiceField(label='Categoría', queryset=Categoria.objects.order_by('nombre'), required=False, empty_label='Todas las categorías')

    def clean(self):
        datos = super().clean()
        desde, hasta = datos.get('desde'), datos.get('hasta')
        if desde and hasta and desde > hasta:
            raise forms.ValidationError('La fecha inicial debe ser anterior o igual a la fecha final.')
        return datos
