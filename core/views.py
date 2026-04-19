from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Perfil, Rol, Producto, Categoria, Carrito, DetalleCarrito


# ─── AUTENTICACIÓN ────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('loginEmail')
        password = request.POST.get('loginPassword')

        # Permitir login con email o username
        try:
            user_obj = User.objects.get(email=username)
            username = user_obj.username
        except User.DoesNotExist:
            pass

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirigir según rol
            try:
                if user.perfil.es_admin():
                    return redirect('admin_panel')
            except Perfil.DoesNotExist:
                pass
            return redirect('index')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'core/login.html')


def registro(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        nombre_completo  = request.POST.get('nombreCompleto', '').strip()
        username         = request.POST.get('username', '').strip()
        email            = request.POST.get('email', '').strip()
        password         = request.POST.get('password', '')
        confirm_pass     = request.POST.get('confirmPassword', '')
        fecha_nacimiento = request.POST.get('fechaNacimiento') or None
        direccion        = request.POST.get('direccion', '').strip()

        if password != confirm_pass:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'core/registro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'core/registro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'core/registro.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=nombre_completo,
            )
            # Obtener o crear rol "usuario" por defecto
            rol_usuario, _ = Rol.objects.get_or_create(
                nombre='usuario',
                defaults={'descripcion': 'Usuario estándar de la tienda'}
            )
            Perfil.objects.create(
                usuario=user,
                rol=rol_usuario,
                nombre_completo=nombre_completo,
                fecha_nacimiento=fecha_nacimiento,
                direccion=direccion,
            )
            messages.success(request, '¡Cuenta creada correctamente! Ya puedes iniciar sesión.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Ocurrió un error al crear la cuenta. Inténtalo de nuevo.')

    return render(request, 'core/registro.html')


def recuperar(request):
    if request.method == 'POST':
        email = request.POST.get('emailRecuperar', '').strip()
        # Lógica simulada — en producción se enviaría un correo real
        if User.objects.filter(email=email).exists():
            messages.success(request, 'Si el correo está registrado, recibirás las instrucciones pronto.')
        else:
            messages.error(request, 'No existe una cuenta con ese correo.')
        return redirect('recuperar')
    return render(request, 'core/recuperar.html')


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
    from django.shortcuts import get_object_or_404
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    return render(request, 'core/ficha-producto.html', {'producto': producto})


# ─── PROTEGIDAS (Solo usuarios autenticados) ──────────────────────────────────

@login_required
def perfil(request):
    try:
        perfil_obj = request.user.perfil
    except Perfil.DoesNotExist:
        perfil_obj = None

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'actualizar_perfil':
            nombre    = request.POST.get('perfilNombre', '').strip()
            email     = request.POST.get('perfilEmail', '').strip()
            fecha     = request.POST.get('perfilFecha') or None
            direccion = request.POST.get('perfilDireccion', '').strip()

            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.error(request, 'El correo electrónico ya está en uso por otra cuenta.')
            else:
                request.user.first_name = nombre
                request.user.email = email
                request.user.save()

                if perfil_obj:
                    perfil_obj.nombre_completo  = nombre
                    perfil_obj.fecha_nacimiento = fecha
                    perfil_obj.direccion        = direccion
                    perfil_obj.save()

                messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')

        elif form_type == 'cambiar_password':
            password_actual    = request.POST.get('passwordActual', '')
            password_nueva     = request.POST.get('passwordNueva', '')
            password_confirmar = request.POST.get('passwordConfirmar', '')

            if not request.user.check_password(password_actual):
                messages.error(request, 'La contraseña actual es incorrecta.')
            elif password_nueva != password_confirmar:
                messages.error(request, 'Las contraseñas nuevas no coinciden.')
            else:
                request.user.set_password(password_nueva)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Contraseña actualizada con éxito.')
            return redirect('perfil')

    return render(request, 'core/perfil.html', {
        'usuario': request.user,
        'perfil':  perfil_obj,
    })


@login_required
def admin_panel(request):
    # Solo administradores pueden acceder
    try:
        if not request.user.perfil.es_admin():
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('index')
    except Perfil.DoesNotExist:
        return redirect('index')
    return render(request, 'core/admin.html')


@login_required
def carrito(request):
    return render(request, 'core/carrito.html')


@login_required
def checkout(request):
    return render(request, 'core/checkout.html')