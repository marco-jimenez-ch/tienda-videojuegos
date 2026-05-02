from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Perfil, Categoria, Producto, Carrito, DetalleCarrito


# ─── CATEGORÍA ────────────────────────────────────────────────────────────────

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Categoria
        fields = ['id', 'nombre', 'descripcion']


# ─── PRODUCTO ─────────────────────────────────────────────────────────────────

class ProductoListSerializer(serializers.ModelSerializer):
    """Versión compacta para listados."""
    categoria_nombre = serializers.CharField(
        source='categoria.nombre', read_only=True
    )

    class Meta:
        model  = Producto
        fields = ['id', 'nombre', 'precio', 'stock', 'imagen',
                  'plataforma', 'activo', 'categoria_nombre']


class ProductoDetailSerializer(serializers.ModelSerializer):
    """Versión completa para la ficha de un producto."""
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model  = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock',
                  'imagen', 'plataforma', 'activo', 'categoria']


# ─── USUARIO / REGISTRO ───────────────────────────────────────────────────────

class RegistroSerializer(serializers.ModelSerializer):
    """Permite crear un usuario desde la API con validación de contraseña."""
    password  = serializers.CharField(write_only=True, required=True,
                                      validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model  = User
        fields = ['username', 'email', 'first_name', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Las contraseñas no coinciden.'}
            )
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {'email': 'El correo electrónico ya está registrado.'}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class PerfilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='usuario.username', read_only=True)
    email    = serializers.CharField(source='usuario.email',    read_only=True)
    rol_nombre = serializers.CharField(source='rol.nombre',     read_only=True)

    class Meta:
        model  = Perfil
        fields = ['username', 'email', 'nombre_completo',
                  'fecha_nacimiento', 'direccion', 'fecha_registro', 'rol_nombre']


# ─── CARRITO ──────────────────────────────────────────────────────────────────

class DetalleCarritoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(
        source='producto.nombre', read_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model  = DetalleCarrito
        fields = ['id', 'producto', 'producto_nombre',
                  'cantidad', 'precio_unitario', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()


class CarritoSerializer(serializers.ModelSerializer):
    detalles = DetalleCarritoSerializer(
        source='detallecarrito_set', many=True, read_only=True
    )
    total = serializers.SerializerMethodField()

    class Meta:
        model  = Carrito
        fields = ['id', 'fecha_creacion', 'activo', 'total', 'detalles']

    def get_total(self, obj):
        return obj.total()