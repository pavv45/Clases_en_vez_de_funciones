# nomina/models.py
from django.db import models
from decimal import Decimal


class Empleado(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=200)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    departamento = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.cedula}"


class Nomina(models.Model):
    aniomes = models.CharField(max_length=6)  # YYYYMM
    tot_ing = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tot_des = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    neto = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        year = self.aniomes[:4]
        month = self.aniomes[4:]
        return f"Nómina {month}/{year}"

    def recalcular_totales(self):
        """Recalcula los totales basado en los detalles"""
        detalles = self.nominadetalle_set.all()
        self.tot_ing = sum(detalle.tot_ing for detalle in detalles)
        self.tot_des = sum(detalle.tot_des for detalle in detalles)
        self.neto = sum(detalle.neto for detalle in detalles)
        self.save()


class NominaDetalle(models.Model):
    nomina = models.ForeignKey(Nomina, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bono = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tot_ing = models.DecimalField(max_digits=10, decimal_places=2)
    iess = models.DecimalField(max_digits=10, decimal_places=2)  # 9.45%
    prestamo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tot_des = models.DecimalField(max_digits=10, decimal_places=2)
    neto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nomina} - {self.empleado.nombre}"

    def save(self, *args, **kwargs):
        from decimal import Decimal

        # Tomar el sueldo desde el empleado directamente
        sueldo = self.empleado.sueldo or Decimal('0.00')
        bono = self.bono or Decimal('0.00')
        prestamo = self.prestamo or Decimal('0.00')

        # Asignar automáticamente el sueldo del empleado
        self.sueldo = sueldo

        # Calcular totales automáticamente
        self.tot_ing = sueldo + bono
        self.iess = (self.tot_ing * Decimal('0.0945')).quantize(Decimal('0.01'))
        self.tot_des = self.iess + prestamo
        self.neto = self.tot_ing - self.tot_des

        super().save(*args, **kwargs)

        # Recalcular totales de la nómina
        self.nomina.recalcular_totales()