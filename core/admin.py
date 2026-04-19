from django.contrib import admin
from .models import Rol, Perfil, Categoria, Producto, Carrito, DetalleCarrito


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display  = ('nombre_completo', 'usuario', 'rol', 'fecha_registro')
    search_fields = ('nombre_completo', 'usuario__username')
    list_filter   = ('rol',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'categoria', 'precio', 'stock', 'activo')
    search_fields = ('nombre',)
    list_filter   = ('categoria', 'activo')


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display  = ('id', 'usuario', 'fecha_creacion', 'activo')
    list_filter   = ('activo',)


@admin.register(DetalleCarrito)
class DetalleCarritoAdmin(admin.ModelAdmin):
    list_display  = ('carrito', 'producto', 'cantidad', 'precio_unitario')