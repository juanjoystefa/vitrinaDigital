from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Rutas de Autenticación
    path("registro/", views.registro, name="registro"),
    path("login/", auth_views.LoginView.as_view(template_name='login/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='/'), name="logout"),

    # Rutas del Panel de Administración
        path("panel/pendientes/", views.admin_pendientes, name="admin_pendientes"),
        path("panel/usuarios/", views.admin_usuarios, name="admin_usuarios"),
        path("panel/emprendimientos/", views.admin_emprendimientos, name="admin_emprendimientos"),

    # Rutas Públicas
    path("emprendimientos/", views.inicio, name="emprendimientos"),
    path("emprendimientos/crear/", views.crear_emprendimiento, name="crear_emprendimiento"),
    path("emprendimientos/editar/<int:id>/", views.editar_emprendimiento, name="editar_emprendimiento"),
    path("emprendimientos/eliminar/<int:id>/", views.eliminar_emprendimiento, name="eliminar_emprendimiento"),
    path('emprendimientos/estado/<int:id>/<str:nuevo_estado>/', views.cambiar_estado_emprendimiento, name='cambiar_estado_emprendimiento'),
    path("visitar/<int:id>/", views.registrar_visita, name="registrar_visita"),
    path("visitar/<int:id>/<str:origen>/", views.registrar_visita, name="registrar_visita_origen"),
    path("accounts/profile/", views.perfil_usuario, name="perfil"),
    
    
]