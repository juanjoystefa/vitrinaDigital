from django.db import models
from django.utils import timezone


print(timezone.now);

class Emprendimiento(models.Model):
    idEmprendimiento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    totalVistas = models.IntegerField(default=0)



class Vistas(models.Model):
    idVisita = models.AutoField(primary_key=True)
    fechaHora = models.DateTimeField(auto_now_add=True)
    idEmprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.CASCADE, related_name="Vistas")

    def save(self, *args, **kwargs):
        # Verificamos si es un registro nuevo (Si no tiene un ID aún)
        es_nuevo = self.pk is None

        # Guardamos la visita primero
        super().save(*args, **kwargs)

        # Si es nueva, le sumamos 1 al emprendimiento asociado
        if es_nuevo:
            self.idEmprendimiento.totalVistas += 1
            self.idEmprendimiento.save()