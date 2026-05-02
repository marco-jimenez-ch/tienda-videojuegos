from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.utils.dateparse import parse_date

from .models import Perfil, Rol, Producto, Categoria, Carrito, DetalleCarrito


# ─── VALIDACIONES DE SERVIDOR ─────────────────────────────────────────────────

def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year

    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1

    return edad


def validar_fecha_nacimiento(fecha_nacimiento):
    if not fecha_nacimiento:
        raise ValidationError('La fecha de nacimiento es obligatoria.')

    fecha = parse_date(fecha_nacimiento)

    if fecha is None:
        raise ValidationError('La fecha de nacimiento no tiene un formato válido.')

    if fecha > date.today():
        raise ValidationError('La fecha de nacimiento no puede ser futura.')

    if calcular_edad(fecha) < 13:
        raise ValidationError('Debes tener al menos 13 años para registrarte.')

    return fecha


def validar_username(username):
    if not username:
        raise ValidationError('El nombre de usuario es obligatorio.')

    if len(username) < 3:
        raise ValidationError('El nombre de usuario debe tener al menos 3 caracteres.')

    if len(username) > 20:
        raise ValidationError('El nombre de usuario no puede superar los 20 caracteres.')

    if any(caracter.isspace() for caracter in username):
        raise ValidationError('El nombre de usuario no puede contener espacios.')


def validar_nombre_completo(nombre_completo):
    if not nombre_completo:
        raise ValidationError('El nombre completo es obligatorio.')

    if len(nombre_completo) < 3:
        raise ValidationError('El nombre completo debe tener al menos 3 caracteres.')


def validar_password_segura(password, user=None):
    validate_password(password, user=user)


def obtener_username_desde_login(login_email_o_usuario):
    valor = (login_email_o_usuario or '').strip()

    if '@' not in valor:
        return valor

    try:
        usuario = User.objects.get(email__iexact=valor)
        return usuario.username
    except User.DoesNotExist:
        return valor
    except MultipleObjectsReturned:
        return None


def usuario_es_admin(user):
    try:
        return user.perfil.es_admin()
    except Perfil.DoesNotExist:
        return False


# ─── AUTENTICACIÓN ────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('loginEmail', '').strip()
        password = request.POST.get('loginPassword', '')

        username = obtener_username_desde_login(username)

        if username is None:
            messages.error(
                request,
                'Existe más de una cuenta asociada a ese correo. Contacta al administrador.'
            )
            return render(request, 'core/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if usuario_es_admin(user):
                return redirect('admin_panel')

            return redirect('index')

        messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'core/login.html')


def registro(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        nombre_completo = request.POST.get('nombreCompleto', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_pass = request.POST.get('confirmPassword', '')
        fecha_nacimiento = request.POST.get('fechaNacimiento') or None
        direccion = request.POST.get('direccion', '').strip()

        errores = []

        try:
            validar_nombre_completo(nombre_completo)
        except ValidationError as error:
            errores.extend(error.messages)

        try:
            validar_username(username)
        except ValidationError as error:
            errores.extend(error.messages)

        if not email:
            errores.append('El correo electrónico es obligatorio.')

        if password != confirm_pass:
            errores.append('Las contraseñas no coinciden.')

        if User.objects.filter(username__iexact=username).exists():
            errores.append('El nombre de usuario ya está en uso.')

        if User.objects.filter(email__iexact=email).exists():
            errores.append('El correo electrónico ya está registrado.')

        try:
            fecha_nacimiento_validada = validar_fecha_nacimiento(fecha_nacimiento)
        except ValidationError as error:
            errores.extend(error.messages)
            fecha_nacimiento_validada = None

        try:
            validar_password_segura(password)
        except ValidationError as error:
            errores.extend(error.messages)

        if errores:
            for error in errores:
                messages.error(request, error)

            return render(request, 'core/registro.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=nombre_completo,
            )

            rol_usuario, _ = Rol.objects.get_or_create(
                nombre='usuario',
                defaults={'descripcion': 'Usuario estándar de la tienda'}
            )

            Perfil.objects.create(
                usuario=user,
                rol=rol_usuario,
                nombre_completo=nombre_completo,
                fecha_nacimiento=fecha_nacimiento_validada,
                direccion=direccion,
            )

            messages.success(request, '¡Cuenta creada correctamente! Ya puedes iniciar sesión.')
            return redirect('login')

        except Exception:
            messages.error(request, 'Ocurrió un error al crear la cuenta. Inténtalo de nuevo.')

    return render(request, 'core/registro.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── CATÁLOGO PÚBLICO ─────────────────────────────────────────────────────────

def index(request):
    return render(request, 'core/index.html')


def accion(request):
    productos = Producto.objects.filter(categoria__nombre='Acción', activo=True)
    return render(request, 'core/accion.html', {'productos': productos})


def aventura(request):
    productos = Producto.objects.filter(categoria__nombre='Aventura', activo=True)
    return render(request, 'core/aventura.html', {'productos': productos})


def fps(request):
    productos = Producto.objects.filter(categoria__nombre='FPS', activo=True)
    return render(request, 'core/fps.html', {'productos': productos})


def deportes(request):
    productos = Producto.objects.filter(categoria__nombre='Deportes', activo=True)
    return render(request, 'core/deportes.html', {'productos': productos})


def rpg(request):
    productos = Producto.objects.filter(categoria__nombre='RPG', activo=True)
    return render(request, 'core/rpg.html', {'productos': productos})


def ficha_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)

    slugs = {
        'Acción': 'accion',
        'Aventura': 'aventura',
        'FPS': 'fps',
        'Deportes': 'deportes',
        'RPG': 'rpg',
    }

    categoria_slug = slugs.get(producto.categoria.nombre, 'accion')

    return render(request, 'core/ficha-producto.html', {
        'producto': producto,
        'categoria_slug': categoria_slug,
    })


# ─── PROTEGIDAS ───────────────────────────────────────────────────────────────

@login_required
def perfil(request):
    try:
        perfil_obj = request.user.perfil
    except Perfil.DoesNotExist:
        perfil_obj = None

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'actualizar_perfil':
            nombre = request.POST.get('perfilNombre', '').strip()
            email = request.POST.get('perfilEmail', '').strip().lower()
            fecha = request.POST.get('perfilFecha') or None
            direccion = request.POST.get('perfilDireccion', '').strip()

            errores = []

            try:
                validar_nombre_completo(nombre)
            except ValidationError as error:
                errores.extend(error.messages)

            if not email:
                errores.append('El correo electrónico es obligatorio.')

            if User.objects.filter(email__iexact=email).exclude(id=request.user.id).exists():
                errores.append('El correo electrónico ya está en uso por otra cuenta.')

            try:
                fecha_validada = validar_fecha_nacimiento(fecha)
            except ValidationError as error:
                errores.extend(error.messages)
                fecha_validada = None

            if errores:
                for error in errores:
                    messages.error(request, error)
            else:
                request.user.first_name = nombre
                request.user.email = email
                request.user.save()

                if perfil_obj:
                    perfil_obj.nombre_completo = nombre
                    perfil_obj.fecha_nacimiento = fecha_validada
                    perfil_obj.direccion = direccion
                    perfil_obj.save()

                messages.success(request, 'Perfil actualizado correctamente.')

            return redirect('perfil')

        elif form_type == 'cambiar_password':
            password_actual = request.POST.get('passwordActual', '')
            password_nueva = request.POST.get('passwordNueva', '')
            password_confirmar = request.POST.get('passwordConfirmar', '')

            if not request.user.check_password(password_actual):
                messages.error(request, 'La contraseña actual es incorrecta.')

            elif password_nueva != password_confirmar:
                messages.error(request, 'Las contraseñas nuevas no coinciden.')

            else:
                try:
                    validar_password_segura(password_nueva, request.user)

                    request.user.set_password(password_nueva)
                    request.user.save()

                    update_session_auth_hash(request, request.user)

                    messages.success(request, 'Contraseña actualizada con éxito.')

                except ValidationError as error:
                    for mensaje in error.messages:
                        messages.error(request, mensaje)

            return redirect('perfil')

    return render(request, 'core/perfil.html', {
        'usuario': request.user,
        'perfil': perfil_obj,
    })


@login_required
def admin_panel(request):
    if not usuario_es_admin(request.user):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('index')

    return render(request, 'core/admin.html')


@login_required
def carrito(request):
    carrito_obj, _ = Carrito.objects.get_or_create(usuario=request.user, activo=True)
    detalles = carrito_obj.detallecarrito_set.select_related('producto').all()
    total = sum(d.subtotal() for d in detalles)

    return render(request, 'core/carrito.html', {
        'carrito': carrito_obj,
        'detalles': detalles,
        'total': total,
    })


@login_required
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)

    carrito_obj, _ = Carrito.objects.get_or_create(usuario=request.user, activo=True)

    detalle, creado = DetalleCarrito.objects.get_or_create(
        carrito=carrito_obj,
        producto=producto,
        defaults={
            'precio_unitario': producto.precio,
            'cantidad': 1
        }
    )

    if not creado:
        detalle.cantidad += 1
        detalle.save()

    messages.success(request, f'"{producto.nombre}" agregado al carrito.')
    return redirect('carrito')


@login_required
def eliminar_carrito(request, detalle_id):
    detalle = get_object_or_404(
        DetalleCarrito,
        id=detalle_id,
        carrito__usuario=request.user
    )

    nombre = detalle.producto.nombre
    detalle.delete()

    messages.success(request, f'"{nombre}" eliminado del carrito.')
    return redirect('carrito')


@login_required
def checkout(request):
    carrito_obj, _ = Carrito.objects.get_or_create(usuario=request.user, activo=True)
    detalles = carrito_obj.detallecarrito_set.select_related('producto').all()
    total = sum(d.subtotal() for d in detalles)

    if request.method == 'POST':
        detalles.delete()
        carrito_obj.activo = False
        carrito_obj.save()

        messages.success(request, '¡Compra realizada con éxito! Gracias por tu pedido.')
        return redirect('index')

    return render(request, 'core/checkout.html', {
        'carrito': carrito_obj,
        'detalles': detalles,
        'total': total,
    })