from django.contrib import admin
from .models import Rol, Perfil


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display  = ('nombre_completo', 'usuario', 'rol', 'fecha_registro')
    search_fields = ('nombre_completo', 'usuario__username')
    list_filter   = ('rol',)
