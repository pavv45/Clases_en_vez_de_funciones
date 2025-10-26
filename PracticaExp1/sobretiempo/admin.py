from django.contrib import admin
from .models import TipoSobretiempo, Sobretiempo

@admin.register(TipoSobretiempo)
class TipoSobretiempoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'factor']
    search_fields = ['codigo', 'descripcion']

@admin.register(Sobretiempo)
class SobretiempoAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'fecha_registro', 'tipo_sobretiempo', 'numero_horas', 'valor']
    list_filter = ['tipo_sobretiempo', 'fecha_registro']
    search_fields = ['empleado__nombre']
    readonly_fields = ['valor']