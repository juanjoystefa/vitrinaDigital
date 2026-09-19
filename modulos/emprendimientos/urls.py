from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path('visitar/<int:id>/', views.registrar_visita, name='registrar_visita'), # <-- Nueva ruta,
    
]