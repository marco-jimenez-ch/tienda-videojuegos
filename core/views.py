from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# ─── PÚBLICAS ────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('loginEmail')
        password = request.POST.get('loginPassword')
        
        # Intentar buscar por email si no funciona como username
        from django.contrib.auth.models import User
        try:
            user_obj = User.objects.get(email=username)
            username = user_obj.username
        except User.DoesNotExist:
            pass
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'core/login.html')


def registro(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'core/registro.html')


def recuperar(request):
    return render(request, 'core/recuperar.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── PROTEGIDAS ──────────────────────────────────────────────────────────────

@login_required
def index(request):
    return render(request, 'core/index.html')


@login_required
def perfil(request):
    return render(request, 'core/perfil.html')


@login_required
def admin_panel(request):
    return render(request, 'core/admin.html')


@login_required
def accion(request):
    return render(request, 'core/accion.html')


@login_required
def aventura(request):
    return render(request, 'core/aventura.html')


@login_required
def fps(request):
    return render(request, 'core/fps.html')


@login_required
def deportes(request):
    return render(request, 'core/deportes.html')


@login_required
def rpg(request):
    return render(request, 'core/rpg.html')


@login_required
def ficha_producto(request):
    return render(request, 'core/ficha-producto.html')


@login_required
def carrito(request):
    return render(request, 'core/carrito.html')


@login_required
def checkout(request):
    return render(request, 'core/checkout.html')