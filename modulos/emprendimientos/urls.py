from django.urls import path
from . import views

urlpatterns = [
    path("emprendimientos/", views.inicio, name="emprendimientos"),
    path('visitar/<int:id>/', views.registrar_visita, name='registrar_visita'), # <-- Nueva ruta,
    
]