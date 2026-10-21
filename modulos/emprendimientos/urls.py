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
    # Emprendimientos
    path("emprendimientos/", views.inicio, name="emprendimientos"),
    path("emprendimientos/<int:id>/", views.detalle_emprendimiento, name="detalle_emprendimiento"),
    path("emprendimientos/crear/", views.crear_emprendimiento, name="crear_emprendimiento"),
    path("emprendimientos/editar/<int:id>/", views.editar_emprendimiento, name="editar_emprendimiento"),
    path("emprendimientos/eliminar/<int:id>/", views.eliminar_emprendimiento, name="eliminar_emprendimiento"),
    path('emprendimientos/estado/<int:id>/<str:nuevo_estado>/', views.cambiar_estado_emprendimiento, name='cambiar_estado_emprendimiento'),

    # Productos
    path("emprendimientos/<int:id_emprendimiento>/productos/crear/", views.crear_producto, name="crear_producto"),
    path("productos/editar/<int:id_producto>/", views.editar_producto, name="editar_producto"),
    path("productos/eliminar/<int:id_producto>/", views.eliminar_producto, name="eliminar_producto"),

    # Rutas de Visitas
    path("visitar/<int:id>/", views.registrar_visita, name="registrar_visita"),
    path("visitar/<int:id>/<str:origen>/", views.registrar_visita, name="registrar_visita_origen"),

    # Ruta del Perfil de Usuario
    path("accounts/profile/", views.perfil_usuario, name="perfil"),
    
    
]