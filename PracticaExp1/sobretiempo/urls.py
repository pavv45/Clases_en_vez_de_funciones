from django.urls import path
from . import views

urlpatterns = [
    path('', views.SobretiempoListView.as_view(), name='sobretiempos_lista'),
    path('nuevo/', views.SobretiempoCreateView.as_view(), name='sobretiempo_crear'),
    path('<int:sobretiempo_id>/', views.SobretiempoDetailView.as_view(), name='sobretiempo_detalle'),
    path('<int:sobretiempo_id>/editar/', views.SobretiempoUpdateView.as_view(), name='sobretiempo_editar'),
    path('<int:sobretiempo_id>/eliminar/', views.SobretiempoDeleteView.as_view(), name='sobretiempo_eliminar'),
    path('empleado/<int:empleado_id>/', views.SobretiemposPorEmpleadoView.as_view(), name='sobretiempos_por_empleado'),
]