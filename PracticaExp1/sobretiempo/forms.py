from django import forms
from .models import Sobretiempo

class SobretiempoForm(forms.ModelForm):
    class Meta:
        model = Sobretiempo
        fields = ['empleado', 'fecha_registro', 'tipo_sobretiempo', 'numero_horas']
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_registro': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_sobretiempo': forms.Select(attrs={'class': 'form-control'}),
            'numero_horas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0'}),
        }
        labels = {
            'empleado': 'Empleado',
            'fecha_registro': 'Fecha de Registro',
            'tipo_sobretiempo': 'Tipo de Sobretiempo',
            'numero_horas': 'Número de Horas',
        }