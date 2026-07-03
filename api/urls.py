from django.urls import path
from . import views

urlpatterns = [
    # Endpoints de Activos
    path('activos/', views.lista_activos, name='lista_activos'),
    path('activos/<int:pk>/', views.detalle_activo, name='detalle_activo'),
    path('tipos-activo/', views.lista_tipos_activo, name='lista_tipos_activo'),
    
    # Endpoints de Autenticación
    path('auth/registro/', views.registro_usuario, name='registro_usuario'),
    path('auth/login/', views.login_usuario, name='login_usuario'),

    # Endpoints de Riesgos, Amenazas y Vulnerabilidades
    path('amenazas/', views.lista_amenazas),
    path('vulnerabilidades/', views.lista_vulnerabilidades),
    path('riesgos/', views.lista_riesgos),
    path('riesgos/<int:pk>/', views.detalle_riesgo),
    path('catalogo-iso/', views.lista_catalogo_iso),
    path('controles-empresa/', views.lista_controles_empresa),
    path('tratamientos/', views.lista_tratamientos),
    path('tratamientos/<int:pk>/', views.detalle_tratamiento),
]