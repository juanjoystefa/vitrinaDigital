from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Rutas de Autenticación
    path("registro/", views.registro, name="registro"),
    path("login/", auth_views.LoginView.as_view(template_name='login/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='/'), name="logout"),

    # Rutas del Panel de Administración
        path("panel/", views.admin_dashboard, name="admin_dashboard"),
        path("panel/estado/<int:id>/<str:nuevo_estado>/", views.cambiar_estado_emprendimiento, name="cambiar_estado"),

    # Rutas Públicas
    path("emprendimientos/", views.inicio, name="emprendimientos"),
    path("visitar/<int:id>/", views.registrar_visita, name="registrar_visita"),
    path("visitar/<int:id>/<str:origen>/", views.registrar_visita, name="registrar_visita_origen"),
    path("accounts/profile/", views.perfil_usuario, name="perfil"),
    
    
]