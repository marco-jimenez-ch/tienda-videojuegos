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


class Categoria(models.Model):
    nombre      = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'DN_CATEGORIA'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria   = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    nombre      = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio      = models.IntegerField(default=0)
    stock       = models.IntegerField(default=0)
    imagen      = models.CharField(max_length=100, blank=True)
    plataforma  = models.CharField(max_length=100, blank=True)
    activo      = models.BooleanField(default=True)

    class Meta:
        db_table = 'DN_PRODUCTO'

    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    usuario       = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo        = models.BooleanField(default=True)

    class Meta:
        db_table = 'DN_CARRITO'

    def __str__(self):
        return f"Carrito #{self.id} — {self.usuario.username}"

    def total(self):
        return sum(d.subtotal() for d in self.detallecarrito_set.all())


class DetalleCarrito(models.Model):
    carrito         = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto        = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad        = models.IntegerField(default=1)
    precio_unitario = models.IntegerField(default=0)

    class Meta:
        db_table = 'DN_DETALLE_CARRITO'

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"

    def subtotal(self):
        return self.cantidad * self.precio_unitario