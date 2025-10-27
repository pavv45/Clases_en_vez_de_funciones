# nomina/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, Avg, Count
from .models import Empleado, Nomina, NominaDetalle
from .forms import EmpleadoForm, NominaForm, NominaDetalleForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import datetime

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Sum, Avg, Count
from .mixins import TitleContextMixin

class DashboardView(LoginRequiredMixin, TitleContextMixin, TemplateView):
    template_name = 'dashboard.html'
    title1 = "Sistema de Nóminas "
    title2 = "Panel Principal"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        context['total_empleados'] = Empleado.objects.count()
        context['total_nominas'] = Nomina.objects.count()
        
        # Nómina del mes actual
        mes_actual = datetime.datetime.now().strftime('%Y%m')
        nomina_mes = Nomina.objects.filter(aniomes=mes_actual).first()
        context['total_nomina_mes'] = nomina_mes.neto if nomina_mes else 0
        
        # Promedio de sueldos
        context['promedio_sueldo'] = Empleado.objects.aggregate(
            promedio=Avg('sueldo')
        )['promedio'] or 0
        
        # Últimos empleados registrados
        context['ultimos_empleados'] = Empleado.objects.order_by('-id')[:5]
        
        # Nóminas recientes
        context['nominas_recientes'] = Nomina.objects.order_by('-aniomes')[:5]
        
        # Estadísticas por departamento
        departamentos_stats = Empleado.objects.values('departamento').annotate(
            total=Count('id')
        ).order_by('-total')
        
        # Calcular porcentajes
        total_emp = context['total_empleados'] if context['total_empleados'] > 0 else 1
        for dept in departamentos_stats:
            dept['porcentaje'] = (dept['total'] / total_emp) * 100
        
        context['departamentos_stats'] = departamentos_stats
        
        return context

# ========== VISTAS DE EMPLEADOS ==========

class EmpleadoListView(LoginRequiredMixin, TitleContextMixin, ListView):
    model = Empleado
    template_name = 'empleados_lista.html'
    context_object_name = 'empleados'
    paginate_by = 10
    title1 = "Empleados"
    title2 = "Listado de Empleados"
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('nombre')
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(cedula__icontains=query) |
                Q(departamento__icontains=query)
            )
        return queryset


class EmpleadoDetailView(LoginRequiredMixin, TitleContextMixin, DetailView):
    model = Empleado
    template_name = 'empleado_detalle.html'
    context_object_name = 'empleado'
    pk_url_kwarg = 'empleado_id'
    title1 = "Empleados"
    title2 = "Detalle del Empleado"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Nóminas del empleado
        context['nominas_empleado'] = NominaDetalle.objects.filter(
            empleado=self.object
        ).order_by('-nomina__aniomes')
        return context


class EmpleadoCreateView(LoginRequiredMixin, TitleContextMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleado_form.html'
    title1 = "Empleados"
    title2 = "Nuevo Empleado"
    
    def get_success_url(self):
        messages.success(
            self.request,
            f'Empleado {self.object.nombre} creado exitosamente.'
        )
        return reverse_lazy('empleado_detalle', kwargs={'empleado_id': self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Empleado'
        return context


class EmpleadoUpdateView(LoginRequiredMixin, TitleContextMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'empleado_form.html'
    pk_url_kwarg = 'empleado_id'
    title1 = "Empleados"
    title2 = "Editar Empleado"
    
    def get_success_url(self):
        messages.success(
            self.request,
            f'Empleado {self.object.nombre} actualizado exitosamente.'
        )
        return reverse_lazy('empleado_detalle', kwargs={'empleado_id': self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar - {self.object.nombre}'
        context['empleado'] = self.object
        return context


class EmpleadoDeleteView(LoginRequiredMixin, TitleContextMixin, DeleteView):
    model = Empleado
    template_name = 'empleado_confirmar_eliminar.html'
    pk_url_kwarg = 'empleado_id'
    success_url = reverse_lazy('empleados_lista')
    title1 = "Empleados"
    title2 = "Eliminar Empleado"
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        nombre = self.object.nombre
        messages.success(
            request,
            f'Empleado {nombre} eliminado exitosamente.'
        )
        return super().delete(request, *args, **kwargs)

# ========== VISTAS DE NÓMINAS ==========

class NominaListView(LoginRequiredMixin, TitleContextMixin, ListView):
    model = Nomina
    template_name = 'nominas_lista.html'
    context_object_name = 'nominas'
    paginate_by = 10
    title1 = "Nóminas"
    title2 = "Listado de Nóminas"
    
    def get_queryset(self):
        return super().get_queryset().order_by('-aniomes')


class NominaDetailView(LoginRequiredMixin, TitleContextMixin, DetailView):
    model = Nomina
    template_name = 'nomina_detalle.html'
    context_object_name = 'nomina'
    pk_url_kwarg = 'nomina_id'
    title1 = "Nóminas"
    title2 = "Detalle de Nómina"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = NominaDetalle.objects.filter(nomina=self.object)
        return context


class NominaCreateView(LoginRequiredMixin, TitleContextMixin, CreateView):
    model = Nomina
    form_class = NominaForm
    template_name = 'nomina_form.html'
    title1 = "Nóminas"
    title2 = "Nueva Nómina"
    
    def get_success_url(self):
        messages.success(
            self.request,
            f'Nómina {self.object} creada exitosamente.'
        )
        return reverse_lazy('nomina_detalle', kwargs={'nomina_id': self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Nómina'
        return context


class NominaUpdateView(LoginRequiredMixin, TitleContextMixin, UpdateView):
    model = Nomina
    form_class = NominaForm
    template_name = 'nomina_form.html'
    pk_url_kwarg = 'nomina_id'
    title1 = "Nóminas"
    title2 = "Editar Nómina"
    
    def get_success_url(self):
        messages.success(
            self.request,
            f'Nómina {self.object} actualizada exitosamente.'
        )
        return reverse_lazy('nomina_detalle', kwargs={'nomina_id': self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar - {self.object}'
        context['nomina'] = self.object
        return context


class NominaDeleteView(LoginRequiredMixin, TitleContextMixin, DeleteView):
    model = Nomina
    template_name = 'nomina_confirmar_eliminar.html'
    pk_url_kwarg = 'nomina_id'
    success_url = reverse_lazy('nominas_lista')
    title1 = "Nóminas"
    title2 = "Eliminar Nómina"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles_count'] = NominaDetalle.objects.filter(nomina=self.object).count()
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        periodo = str(self.object)
        messages.success(
            request,
            f'Nómina {periodo} eliminada exitosamente.'
        )
        return super().delete(request, *args, **kwargs)


class NominaDetalleCreateView(LoginRequiredMixin, TitleContextMixin, CreateView):
    model = NominaDetalle
    form_class = NominaDetalleForm
    template_name = 'nomina_detalle_form.html'
    title1 = "Nóminas"
    title2 = "Agregar Empleado a Nómina"
    
    def dispatch(self, request, *args, **kwargs):
        self.nomina = get_object_or_404(Nomina, id=kwargs['nomina_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nomina'] = self.nomina
        context['titulo'] = f'Agregar Empleado a {self.nomina}'
        return context
    
    def form_valid(self, form):
        # Verificar si el empleado ya está en esta nómina
        empleado = form.cleaned_data['empleado']
        if NominaDetalle.objects.filter(nomina=self.nomina, empleado=empleado).exists():
            messages.error(
                self.request,
                f'El empleado {empleado.nombre} ya está agregado a esta nómina.'
            )
            return self.form_invalid(form)
        
        form.instance.nomina = self.nomina
        messages.success(
            self.request,
            f'Empleado {empleado.nombre} agregado a la nómina exitosamente.'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('nomina_detalle', kwargs={'nomina_id': self.nomina.id})

# ========== VISTA DE REPORTES ==========

class ReportesView(LoginRequiredMixin, TitleContextMixin, TemplateView):
    template_name = 'reportes.html'
    title1 = "Reportes"
    title2 = "Reportes del Sistema"

# Vista de registro
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

# Vista de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista de logout
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión')
    return redirect('login')