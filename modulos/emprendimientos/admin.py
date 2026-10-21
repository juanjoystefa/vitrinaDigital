from django.contrib import admin
from .models import Perfil, Emprendimiento, Vistas, Productos

# Registramos las tablas para que aparezcan en el panel
admin.site.register(Perfil)
admin.site.register(Emprendimiento)
admin.site.register(Vistas)
admin.site.register(Productos)