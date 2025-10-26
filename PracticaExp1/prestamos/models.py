from django.db import models
from nomina.models import Empleado
from decimal import Decimal  # ← AGREGAR ESTE IMPORT


class TipoPrestamo(models.Model):
    descripcion = models.CharField(max_length=100)
    tasa = models.IntegerField(default=0)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = "Tipo de Préstamo"
        verbose_name_plural = "Tipos de Préstamo"


class Prestamo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo_prestamo = models.ForeignKey(TipoPrestamo, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monto_pagar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    numero_cuotas = models.PositiveIntegerField(default=1)
    cuota_mensual = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)

    def save(self, *args, **kwargs):
        # Calcular interés: monto * (tasa/100)
        tasa_decimal = Decimal(str(self.tipo_prestamo.tasa)) / Decimal('100')
        self.interes = self.monto * tasa_decimal

        # Calcular monto a pagar: monto + interés
        self.monto_pagar = self.monto + self.interes

        # Calcular cuota mensual: monto_pagar / numero_cuotas
        if self.numero_cuotas > 0:
            self.cuota_mensual = self.monto_pagar / Decimal(str(self.numero_cuotas))
        else:
            self.cuota_mensual = Decimal('0')

        # Saldo inicial es igual al monto a pagar
        if not self.pk:  # Solo si es un préstamo nuevo
            self.saldo = self.monto_pagar

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Préstamo de {self.empleado.nombre} - {self.tipo_prestamo.descripcion}"

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ['-fecha_prestamo']