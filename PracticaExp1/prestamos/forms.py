from django import forms
from .models import Prestamo

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['empleado', 'tipo_prestamo', 'fecha_prestamo', 'monto', 'numero_cuotas']
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'tipo_prestamo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_prestamo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'numero_cuotas': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
        labels = {
            'empleado': 'Empleado',
            'tipo_prestamo': 'Tipo de Préstamo',
            'fecha_prestamo': 'Fecha del Préstamo',
            'monto': 'Monto ($)',
            'numero_cuotas': 'Número de Cuotas',
        }