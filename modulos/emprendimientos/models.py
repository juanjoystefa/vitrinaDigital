from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1. Modelo para gestionar los roles de los usuarios
class Perfil(models.Model):
    ROLES = (
        ('visitante', 'Visitante'),
        ('emprendedor', 'Emprendedor'),
        ('admin', 'Administrador'),
    )
    # Vinculamos este perfil al usuario nativo de Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='visitante')

    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"

    # Esta señal se ejecuta automáticamente cada vez que se guarda un User nuevo
    @receiver(post_save, sender=User)
    def crear_perfil_usuario(sender, instance, created, **kwargs):
        if created:
            # Si el usuario fue creado por consola con createsuperuser, será admin. 
            # Si fue por la página web, será visitante.
            rol_asignado = 'admin' if instance.is_superuser else 'visitante'
            Perfil.objects.create(usuario=instance, rol=rol_asignado)


# 2. Modelo de Emprendimientos actualizado
class Emprendimiento(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('activo', 'Activo'),
        ('rechazado', 'Rechazado'),
    )
    
    idEmprendimiento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True) # Para que el admin sepa de qué trata
    creador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="emprendimientos")
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Redes sociales / Enlaces de contacto
    link_whatsapp = models.CharField(max_length=20, blank=True, null=True, help_text="Solo números")
    link_instagram = models.URLField(blank=True, null=True)
    link_web = models.URLField(blank=True, null=True)

    # Contadores de visitas (Para que el panel cargue súper rápido sin calcular todo el tiempo)
    totalVistas = models.IntegerField(default=0)
    vistas_wa = models.IntegerField(default=0)
    vistas_ig = models.IntegerField(default=0)
    vistas_web = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre


# 3. Modelo de Vistas actualizado con desglose por canal
class Vistas(models.Model):
    ORIGEN_CHOICES = (
        ('general', 'Vista a la tarjeta'),
        ('wa', 'Clic a WhatsApp'),
        ('ig', 'Clic a Instagram'),
        ('web', 'Clic a Página Web'),
    )
    
    idVisita = models.AutoField(primary_key=True)
    fechaHora = models.DateTimeField(auto_now_add=True)
    idEmprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.CASCADE, related_name="Vistas")
    origen = models.CharField(max_length=20, choices=ORIGEN_CHOICES, default='general')

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        super().save(*args, **kwargs)

        # Actualizamos los contadores del Emprendimiento automáticamente
        if es_nuevo:
            # Siempre sumamos 1 a las vistas totales
            self.idEmprendimiento.totalVistas += 1
            
            # Sumamos 1 al canal específico según donde hizo clic
            if self.origen == 'wa':
                self.idEmprendimiento.vistas_wa += 1
            elif self.origen == 'ig':
                self.idEmprendimiento.vistas_ig += 1
            elif self.origen == 'web':
                self.idEmprendimiento.vistas_web += 1
                
            self.idEmprendimiento.save()