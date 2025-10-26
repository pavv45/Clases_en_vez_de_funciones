# nomina/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('empleados/', views.empleados_lista, name='empleados_lista'),
    path('empleados/nuevo/', views.empleado_crear, name='empleado_crear'),
    path('empleados/<int:empleado_id>/', views.empleado_detalle, name='empleado_detalle'),
    path('empleados/<int:empleado_id>/editar/', views.empleado_editar, name='empleado_editar'),
    path('empleados/<int:empleado_id>/eliminar/', views.empleado_eliminar, name='empleado_eliminar'),
    path('nominas/', views.nominas_lista, name='nominas_lista'),
    path('nominas/nueva/', views.nomina_crear, name='nomina_crear'),
    path('nominas/<int:nomina_id>/', views.nomina_detalle, name='nomina_detalle'),
    path('nominas/<int:nomina_id>/editar/', views.nomina_editar, name='nomina_editar'),
    path('nominas/<int:nomina_id>/eliminar/', views.nomina_eliminar, name='nomina_eliminar'),
    path('nominas/<int:nomina_id>/agregar-empleado/', views.nomina_detalle_crear, name='nomina_detalle_crear'),
    path('reportes/', views.reportes, name='reportes'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
]