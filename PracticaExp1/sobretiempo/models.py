from django.db import models
from nomina.models import Empleado
from decimal import Decimal


class TipoSobretiempo(models.Model):
    codigo = models.CharField(max_length=10)  # Ej: "H50", "H100"
    descripcion = models.CharField(max_length=100)  # Ej: "Horas al 50%", "Horas al 100%"
    factor = models.DecimalField(max_digits=4, decimal_places=2)  # Ej: 1.50, 2.00

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = "Tipo de Sobretiempo"
        verbose_name_plural = "Tipos de Sobretiempo"


class Sobretiempo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_registro = models.DateField()
    tipo_sobretiempo = models.ForeignKey(TipoSobretiempo, on_delete=models.CASCADE)
    numero_horas = models.DecimalField(max_digits=6, decimal_places=2)
    valor = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)

    def save(self, *args, **kwargs):
        # Calcular valor del sobretiempo
        # valor = (sueldo_mensual / horas_mensuales) * numero_horas * factor
        horas_mensuales = Decimal('240')  # 240 horas mensuales por defecto

        valor_hora = self.empleado.sueldo / horas_mensuales
        self.valor = valor_hora * self.numero_horas * self.tipo_sobretiempo.factor

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sobretiempo de {self.empleado.nombre} - {self.tipo_sobretiempo.descripcion}"

    class Meta:
        verbose_name = "Sobretiempo"
        verbose_name_plural = "Sobretiempos"
        ordering = ['-fecha_registro']