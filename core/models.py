from django.db import models
from django.contrib.auth.models import User


class Rol(models.Model):
    nombre      = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'DN_ROL'

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    usuario          = models.OneToOneField(User, on_delete=models.CASCADE)
    rol              = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_completo  = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion        = models.CharField(max_length=255, blank=True)
    fecha_registro   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'DN_PERFIL'

    def __str__(self):
        return self.nombre_completo

    def es_admin(self):
        return self.rol and self.rol.nombre.lower() == 'administrador'
