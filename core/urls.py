from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('recuperar/', views.recuperar, name='recuperar'),
    path('perfil/', views.perfil, name='perfil'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('accion/', views.accion, name='accion'),
    path('aventura/', views.aventura, name='aventura'),
    path('fps/', views.fps, name='fps'),
    path('deportes/', views.deportes, name='deportes'),
    path('rpg/', views.rpg, name='rpg'),
    path('ficha-producto/', views.ficha_producto, name='ficha_producto'),
    path('carrito/', views.carrito, name='carrito'),
    path('checkout/', views.checkout, name='checkout'),
]