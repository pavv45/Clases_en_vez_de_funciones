from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Sobretiempo, TipoSobretiempo
from .forms import SobretiempoForm
from nomina.models import Empleado

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Sobretiempo, TipoSobretiempo
from .forms import SobretiempoForm
from nomina.models import Empleado
from .mixins import TitleContextMixin


class SobretiempoListView(LoginRequiredMixin, TitleContextMixin, ListView):
    model = Sobretiempo
    template_name = 'sobretiempos_lista.html'
    context_object_name = 'sobretiempos'
    paginate_by = 10
    title1 = "Sobretiempos"
    title2 = "Gestión de Sobretiempos"
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('empleado', 'tipo_sobretiempo')
        
        # Filtros
        tipo_filtro = self.request.GET.get('tipo')
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        empleado_filtro = self.request.GET.get('empleado')
        
        if tipo_filtro:
            queryset = queryset.filter(tipo_sobretiempo_id=tipo_filtro)
        if fecha_desde:
            queryset = queryset.filter(fecha_registro__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_registro__lte=fecha_hasta)
        if empleado_filtro:
            queryset = queryset.filter(empleado_id=empleado_filtro)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_sobretiempo'] = TipoSobretiempo.objects.all()
        context['empleados'] = Empleado.objects.all()
        return context


class SobretiempoCreateView(LoginRequiredMixin, TitleContextMixin, CreateView):
    model = Sobretiempo
    form_class = SobretiempoForm
    template_name = 'sobretiempo_form.html'
    title1 = "Sobretiempos"
    title2 = "Nuevo Sobretiempo"
    
    def get_success_url(self):
        messages.success(
            self.request,
            f'Sobretiempo registrado exitosamente para {self.object.empleado.nombre}.'
        )
        return reverse_lazy('sobretiempo_detalle', kwargs={'sobretiempo_id': self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Sobretiempo'
        return context


class SobretiempoDetailView(LoginRequiredMixin, TitleContextMixin, DetailView):
    model = Sobretiempo
    template_name = 'sobretiempo_detalle.html'
    context_object_name = 'sobretiempo'
    pk_url_kwarg = 'sobretiempo_id'
    title1 = "Sobretiempos"
    title2 = "Detalle del Sobretiempo"


class SobretiempoUpdateView(LoginRequiredMixin, TitleContextMixin, UpdateView):
    model = Sobretiempo
    form_class = SobretiempoForm
    template_name = 'sobretiempo_form.html'
    pk_url_kwarg = 'sobretiempo_id'
    title1 = "Sobretiempos"
    title2 = "Editar Sobretiempo"
    
    def get_success_url(self):
        messages.success(
            self.request,
            f'Sobretiempo actualizado exitosamente.'
        )
        return reverse_lazy('sobretiempo_detalle', kwargs={'sobretiempo_id': self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar - Sobretiempo #{self.object.id}'
        context['sobretiempo'] = self.object
        return context


class SobretiempoDeleteView(LoginRequiredMixin, TitleContextMixin, DeleteView):
    model = Sobretiempo
    template_name = 'sobretiempo_confirmar_eliminar.html'
    pk_url_kwarg = 'sobretiempo_id'
    success_url = reverse_lazy('sobretiempos_lista')
    title1 = "Sobretiempos"
    title2 = "Eliminar Sobretiempo"
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        empleado_nombre = self.object.empleado.nombre
        messages.success(
            request,
            f'Sobretiempo de {empleado_nombre} eliminado exitosamente.'
        )
        return super().delete(request, *args, **kwargs)


class SobretiemposPorEmpleadoView(LoginRequiredMixin, TitleContextMixin, DetailView):
    model = Empleado
    template_name = 'sobretiempos_por_empleado.html'
    context_object_name = 'empleado'
    pk_url_kwarg = 'empleado_id'
    title1 = "Sobretiempos"
    title2 = "Sobretiempos por Empleado"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sobretiempos = Sobretiempo.objects.filter(
            empleado=self.object
        ).select_related('tipo_sobretiempo')
        
        context['sobretiempos'] = sobretiempos
        
        # Calcular totales
        context['total_horas'] = sum([st.numero_horas for st in sobretiempos])
        context['total_valor'] = sum([st.valor for st in sobretiempos])
        
        return context