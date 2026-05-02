from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import api_views

urlpatterns = [

    # ── JWT — Autenticación ───────────────────────────────────────────
    # POST /api/token/          → { "username": "...", "password": "..." }
    # Devuelve: { "access": "...", "refresh": "..." }
    path('token/',         TokenObtainPairView.as_view(),  name='api_token'),

    # POST /api/token/refresh/  → { "refresh": "..." }
    # Devuelve: { "access": "..." }  (nuevo access token)
    path('token/refresh/', TokenRefreshView.as_view(),     name='api_token_refresh'),

    # ── APIs propias ─────────────────────────────────────────────────
    path('productos/',          api_views.ProductoListAPIView.as_view(),   name='api_productos'),
    path('productos/<int:pk>/', api_views.ProductoDetailAPIView.as_view(), name='api_producto_detail'),
    path('registro/',           api_views.RegistroAPIView.as_view(),       name='api_registro'),
    path('perfil/',             api_views.PerfilAPIView.as_view(),         name='api_perfil'),
    path('carrito/',            api_views.CarritoAPIView.as_view(),        name='api_carrito'),

    # ── APIs externas consumidas ─────────────────────────────────────
    path('juegos-externos/',    api_views.juegos_freetogame,               name='api_freetogame'),
    path('juegos-rawg/',        api_views.juegos_rawg,                     name='api_rawg'),
]