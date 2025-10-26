from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Prestamo, TipoPrestamo
from .forms import PrestamoForm
from nomina.models import Empleado

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Prestamo, TipoPrestamo
from .forms import PrestamoForm
from nomina.models import Empleado
from .mixins import TitleContextMixin


class PrestamoListView(LoginRequiredMixin, TitleContextMixin, ListView):
    model = Prestamo
    template_name = 'prestamos_lista.html'
    context_object_name = 'prestamos'
    paginate_by = 10
    title1 = "Préstamos"
    title2 = "Gestión de Préstamos"
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('empleado', 'tipo_prestamo')
        
        # Filtros
        tipo_filtro = self.request.GET.get('tipo')
        fecha_filtro = self.request.GET.get('fecha')
        empleado_filtro = self.request.GET.get('empleado')
        
        if tipo_filtro:
            queryset = queryset.filter(tipo_prestamo_id=tipo_filtro)
        if fecha_filtro:
            queryset = queryset.filter(fecha_prestamo=fecha_filtro)
        if empleado_filtro:
            queryset = queryset.filter(empleado_id=empleado_filtro)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_prestamo'] = TipoPrestamo.objects.all()
        context['empleados'] = Empleado.objects.all()
        return context


class PrestamoCreateView(LoginRequiredMixin, TitleContextMixin, CreateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'prestamo_form.html'
    title1 = "Préstamos"
    title2 = "Nuevo Préstamo"
    
    def get_success_url(self):
        messages.success(
            self.request,
            f'Préstamo creado exitosamente para {self.object.empleado.nombre}.'
        )
        return reverse_lazy('prestamo_detalle', kwargs={'prestamo_id': self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Préstamo'
        return context


class PrestamoDetailView(LoginRequiredMixin, TitleContextMixin, DetailView):
    model = Prestamo
    template_name = 'prestamo_detalle.html'
    context_object_name = 'prestamo'
    pk_url_kwarg = 'prestamo_id'
    title1 = "Préstamos"
    title2 = "Detalle del Préstamo"


class PrestamoUpdateView(LoginRequiredMixin, TitleContextMixin, UpdateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'prestamo_form.html'
    pk_url_kwarg = 'prestamo_id'
    title1 = "Préstamos"
    title2 = "Editar Préstamo"
    
    def get_success_url(self):
        messages.success(
            self.request,
            f'Préstamo actualizado exitosamente.'
        )
        return reverse_lazy('prestamo_detalle', kwargs={'prestamo_id': self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar - Préstamo #{self.object.id}'
        context['prestamo'] = self.object
        return context


class PrestamoDeleteView(LoginRequiredMixin, TitleContextMixin, DeleteView):
    model = Prestamo
    template_name = 'prestamo_confirmar_eliminar.html'
    pk_url_kwarg = 'prestamo_id'
    success_url = reverse_lazy('prestamos_lista')
    title1 = "Préstamos"
    title2 = "Eliminar Préstamo"
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        empleado_nombre = self.object.empleado.nombre
        messages.success(
            request,
            f'Préstamo de {empleado_nombre} eliminado exitosamente.'
        )
        return super().delete(request, *args, **kwargs)


class PrestamosPorEmpleadoView(LoginRequiredMixin, TitleContextMixin, DetailView):
    model = Empleado
    template_name = 'prestamos_por_empleado.html'
    context_object_name = 'empleado'
    pk_url_kwarg = 'empleado_id'
    title1 = "Préstamos"
    title2 = "Préstamos por Empleado"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prestamos'] = Prestamo.objects.filter(
            empleado=self.object
        ).select_related('tipo_prestamo')
        return context