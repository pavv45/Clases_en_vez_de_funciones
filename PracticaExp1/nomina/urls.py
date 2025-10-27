from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Empleados
    path('empleados/', views.EmpleadoListView.as_view(), name='empleados_lista'),
    path('empleados/nuevo/', views.EmpleadoCreateView.as_view(), name='empleado_crear'),
    path('empleados/<int:empleado_id>/', views.EmpleadoDetailView.as_view(), name='empleado_detalle'),
    path('empleados/<int:empleado_id>/editar/', views.EmpleadoUpdateView.as_view(), name='empleado_editar'),
    path('empleados/<int:empleado_id>/eliminar/', views.EmpleadoDeleteView.as_view(), name='empleado_eliminar'),
    
    # Nóminas
    path('nominas/', views.NominaListView.as_view(), name='nominas_lista'),
    path('nominas/nueva/', views.NominaCreateView.as_view(), name='nomina_crear'),
    path('nominas/<int:nomina_id>/', views.NominaDetailView.as_view(), name='nomina_detalle'),
    path('nominas/<int:nomina_id>/editar/', views.NominaUpdateView.as_view(), name='nomina_editar'),
    path('nominas/<int:nomina_id>/eliminar/', views.NominaDeleteView.as_view(), name='nomina_eliminar'),
    path('nominas/<int:nomina_id>/agregar-empleado/', views.NominaDetalleCreateView.as_view(), name='nomina_detalle_crear'),
    
    # Reportes
    path('reportes/', views.ReportesView.as_view(), name='reportes'),
]