# nomina/admin.py
from django.contrib import admin
from .models import Empleado, Nomina, NominaDetalle

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['cedula', 'nombre', 'departamento', 'cargo', 'sueldo']
    search_fields = ['cedula', 'nombre', 'departamento']

@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = ['aniomes', 'tot_ing', 'tot_des', 'neto']
    readonly_fields = ['tot_ing', 'tot_des', 'neto']

@admin.register(NominaDetalle)
class NominaDetalleAdmin(admin.ModelAdmin):
    list_display = ['nomina', 'empleado', 'sueldo', 'bono', 'tot_ing', 'iess', 'prestamo', 'tot_des', 'neto']
    readonly_fields = ['tot_ing', 'iess', 'tot_des', 'neto']