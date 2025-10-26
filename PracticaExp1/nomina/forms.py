# nomina/forms.py
from django import forms
from .models import Empleado, Nomina, NominaDetalle


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['cedula', 'nombre', 'sueldo', 'departamento', 'cargo']
        widgets = {
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese número de cédula',
                'maxlength': '10',
                'pattern': '[0-9]{1,10}'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del empleado'
            }),
            'sueldo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'departamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Recursos Humanos, Contabilidad'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Analista, Gerente, Asistente'
            }),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula debe contener solo números.")
        if len(cedula) < 8:
            raise forms.ValidationError("La cédula debe tener al menos 8 dígitos.")
        return cedula

    def clean_sueldo(self):
        sueldo = self.cleaned_data['sueldo']
        if sueldo <= 0:
            raise forms.ValidationError("El sueldo debe ser mayor a 0.")
        return sueldo


class NominaForm(forms.ModelForm):
    class Meta:
        model = Nomina
        fields = ['aniomes']
        widgets = {
            'aniomes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYYMM (Ej: 202501)',
                'pattern': '[0-9]{6}',
                'maxlength': '6'
            }),
        }

    def clean_aniomes(self):
        aniomes = self.cleaned_data['aniomes']
        if not aniomes.isdigit() or len(aniomes) != 6:
            raise forms.ValidationError("El formato debe ser YYYYMM (6 dígitos).")

        year = int(aniomes[:4])
        month = int(aniomes[4:])

        if year < 2020 or year > 2030:
            raise forms.ValidationError("El año debe estar entre 2020 y 2030.")

        if month < 1 or month > 12:
            raise forms.ValidationError("El mes debe estar entre 01 y 12.")

        # Verificar si ya existe una nómina para ese período
        if Nomina.objects.filter(aniomes=aniomes).exists():
            raise forms.ValidationError(f"Ya existe una nómina para el período {aniomes}.")

        return aniomes


class NominaDetalleForm(forms.ModelForm):
    class Meta:
        model = NominaDetalle
        fields = ['empleado', 'bono', 'prestamo']
        widgets = {
            'empleado': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Seleccione un empleado'
            }),
            'bono': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'value': '0.00',
                'placeholder': '0.00'
            }),
            'prestamo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'value': '0.00',
                'placeholder': '0.00'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empleado'].queryset = Empleado.objects.all()
        self.fields['empleado'].empty_label = "Seleccione un empleado"

    def clean_bono(self):
        bono = self.cleaned_data['bono']
        if bono < 0:
            raise forms.ValidationError("El bono no puede ser negativo.")
        return bono

    def clean_prestamo(self):
        prestamo = self.cleaned_data['prestamo']
        if prestamo < 0:
            raise forms.ValidationError("El préstamo no puede ser negativo.")
        return prestamo
