from django.urls import path
from . import views

urlpatterns = [
    path('', views.PrestamoListView.as_view(), name='prestamos_lista'),
    path('nuevo/', views.PrestamoCreateView.as_view(), name='prestamo_crear'),
    path('<int:prestamo_id>/', views.PrestamoDetailView.as_view(), name='prestamo_detalle'),
    path('<int:prestamo_id>/editar/', views.PrestamoUpdateView.as_view(), name='prestamo_editar'),
    path('<int:prestamo_id>/eliminar/', views.PrestamoDeleteView.as_view(), name='prestamo_eliminar'),
    path('empleado/<int:empleado_id>/', views.PrestamosPorEmpleadoView.as_view(), name='prestamos_por_empleado'),
]