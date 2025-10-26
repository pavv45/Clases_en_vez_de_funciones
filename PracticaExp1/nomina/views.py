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

@login_required
def dashboard(request):
    """Vista principal del dashboard"""
    # Estadísticas generales
    total_empleados = Empleado.objects.count()
    total_nominas = Nomina.objects.count()

    # Nómina del mes actual
    mes_actual = datetime.datetime.now().strftime('%Y%m')
    nomina_mes = Nomina.objects.filter(aniomes=mes_actual).first()
    total_nomina_mes = nomina_mes.neto if nomina_mes else 0

    # Promedio de sueldos
    promedio_sueldo = Empleado.objects.aggregate(
        promedio=Avg('sueldo')
    )['promedio'] or 0

    # Últimos empleados registrados
    ultimos_empleados = Empleado.objects.order_by('-id')[:5]

    # Nóminas recientes
    nominas_recientes = Nomina.objects.order_by('-aniomes')[:5]

    # Estadísticas por departamento
    departamentos_stats = Empleado.objects.values('departamento').annotate(
        total=Count('id')
    ).order_by('-total')

    # Calcular porcentajes
    total_emp = total_empleados if total_empleados > 0 else 1
    for dept in departamentos_stats:
        dept['porcentaje'] = (dept['total'] / total_emp) * 100

    context = {
        'total_empleados': total_empleados,
        'total_nominas': total_nominas,
        'total_nomina_mes': total_nomina_mes,
        'promedio_sueldo': promedio_sueldo,
        'ultimos_empleados': ultimos_empleados,
        'nominas_recientes': nominas_recientes,
        'departamentos_stats': departamentos_stats,
    }

    return render(request, 'dashboard.html', context)

@login_required
def empleados_lista(request):
    """Lista de empleados"""
    empleados = Empleado.objects.all().order_by('nombre')

    context = {
        'empleados': empleados,
    }

    return render(request, 'empleados_lista.html', context)

@login_required
def empleado_detalle(request, empleado_id):
    """Detalle de un empleado específico"""
    empleado = get_object_or_404(Empleado, id=empleado_id)

    # Nóminas del empleado
    nominas_empleado = NominaDetalle.objects.filter(
        empleado=empleado
    ).order_by('-nomina__aniomes')

    context = {
        'empleado': empleado,
        'nominas_empleado': nominas_empleado,
    }

    return render(request, 'empleado_detalle.html', context)

@login_required
def empleado_crear(request):
    """Crear nuevo empleado"""
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save()
            messages.success(
                request,
                f'Empleado {empleado.nombre} creado exitosamente.'
            )
            return redirect('empleado_detalle', empleado_id=empleado.id)
    else:
        form = EmpleadoForm()

    context = {'form': form, 'titulo': 'Nuevo Empleado'}
    return render(request, 'empleado_form.html', context)

@login_required
def empleado_editar(request, empleado_id):
    """Editar empleado existente"""
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            empleado = form.save()
            messages.success(
                request,
                f'Empleado {empleado.nombre} actualizado exitosamente.'
            )
            return redirect('empleado_detalle', empleado_id=empleado.id)
    else:
        form = EmpleadoForm(instance=empleado)

    context = {
        'form': form,
        'empleado': empleado,
        'titulo': f'Editar - {empleado.nombre}'
    }
    return render(request, 'empleado_form.html', context)

@login_required
def empleado_eliminar(request, empleado_id):
    """Eliminar empleado"""
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if request.method == 'POST':
        nombre = empleado.nombre
        empleado.delete()
        messages.success(
            request,
            f'Empleado {nombre} eliminado exitosamente.'
        )
        return redirect('empleados_lista')

    context = {'empleado': empleado}
    return render(request, 'empleado_confirmar_eliminar.html', context)

@login_required
def nominas_lista(request):
    """Lista de nóminas"""
    nominas = Nomina.objects.all().order_by('-aniomes')

    context = {
        'nominas': nominas,
    }

    return render(request, 'nominas_lista.html', context)

@login_required
def nomina_crear(request):
    """Crear nueva nómina"""
    if request.method == 'POST':
        form = NominaForm(request.POST)
        if form.is_valid():
            nomina = form.save()
            messages.success(
                request,
                f'Nómina {nomina} creada exitosamente.'
            )
            return redirect('nomina_detalle', nomina_id=nomina.id)
    else:
        form = NominaForm()

    context = {'form': form, 'titulo': 'Nueva Nómina'}
    return render(request, 'nomina_form.html', context)

@login_required
def nomina_detalle(request, nomina_id):
    """Detalle de una nómina específica"""
    nomina = get_object_or_404(Nomina, id=nomina_id)
    detalles = NominaDetalle.objects.filter(nomina=nomina)

    context = {
        'nomina': nomina,
        'detalles': detalles,
    }

    return render(request, 'nomina_detalle.html', context)

@login_required
def nomina_editar(request, nomina_id):
    """Editar nómina existente"""
    nomina = get_object_or_404(Nomina, id=nomina_id)

    if request.method == 'POST':
        form = NominaForm(request.POST, instance=nomina)
        if form.is_valid():
            nomina = form.save()
            messages.success(
                request,
                f'Nómina {nomina} actualizada exitosamente.'
            )
            return redirect('nomina_detalle', nomina_id=nomina.id)
    else:
        form = NominaForm(instance=nomina)

    context = {
        'form': form,
        'nomina': nomina,
        'titulo': f'Editar - {nomina}'
    }
    return render(request, 'nomina_form.html', context)

@login_required
def nomina_eliminar(request, nomina_id):
    """Eliminar nómina"""
    nomina = get_object_or_404(Nomina, id=nomina_id)

    if request.method == 'POST':
        periodo = str(nomina)
        nomina.delete()
        messages.success(
            request,
            f'Nómina {periodo} eliminada exitosamente.'
        )
        return redirect('nominas_lista')

    # Obtener información adicional para mostrar en la confirmación
    detalles_count = NominaDetalle.objects.filter(nomina=nomina).count()

    context = {
        'nomina': nomina,
        'detalles_count': detalles_count
    }
    return render(request, 'nomina_confirmar_eliminar.html', context)

@login_required
def nomina_detalle_crear(request, nomina_id):
    """Crear detalle de nómina para un empleado"""
    nomina = get_object_or_404(Nomina, id=nomina_id)

    if request.method == 'POST':
        form = NominaDetalleForm(request.POST)
        if form.is_valid():
            # Verificar si el empleado ya está en esta nómina
            empleado = form.cleaned_data['empleado']
            if NominaDetalle.objects.filter(nomina=nomina, empleado=empleado).exists():
                messages.error(
                    request,
                    f'El empleado {empleado.nombre} ya está agregado a esta nómina.'
                )
            else:
                detalle = form.save(commit=False)
                detalle.nomina = nomina
                detalle.save()
                messages.success(
                    request,
                    f'Empleado {detalle.empleado.nombre} agregado a la nómina exitosamente.'
                )
                return redirect('nomina_detalle', nomina_id=nomina.id)
    else:
        form = NominaDetalleForm()

    context = {
        'form': form,
        'nomina': nomina,
        'titulo': f'Agregar Empleado a {nomina}'
    }
    return render(request, 'nomina_detalle_form.html', context)

@login_required
def reportes(request):
    """Página de reportes"""
    context = {}
    return render(request, 'reportes.html', context)

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