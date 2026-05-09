"""
APIs REST propias:
  1. /api/productos/          GET  — lista pública con filtro por categoría
  2. /api/productos/<id>/     GET  — detalle de un producto
  3. /api/registro/           POST — registro de usuario
  4. /api/perfil/             GET  — perfil del usuario autenticado
  5. /api/carrito/            GET  — carrito del usuario autenticado

APIs externas consumidas:
  6. /api/juegos-externos/    GET  — juegos desde FreeToGame API
  7. /api/juegos-rawg/        GET  — juegos desde RAWG API
"""

import os
import requests
from rest_framework                 import generics, status
from rest_framework.views           import APIView
from rest_framework.response        import Response
from rest_framework.permissions     import IsAuthenticated, AllowAny
from rest_framework.decorators      import api_view, permission_classes

from .models       import Producto, Carrito
from .serializers  import (
    ProductoListSerializer, ProductoDetailSerializer,
    RegistroSerializer, PerfilSerializer, CarritoSerializer,
)


# ──────────────────────────────────────────────────────────────────────────────
# APIs PROPIAS
# ──────────────────────────────────────────────────────────────────────────────

class ProductoListAPIView(generics.ListAPIView):
    """
    GET /api/productos/
    Lista todos los productos activos.
    Parámetro opcional: ?categoria=RPG
    Permiso: público (no requiere token)
    """
    serializer_class   = ProductoListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Producto.objects.filter(activo=True).select_related('categoria')
        categoria = self.request.query_params.get('categoria')
        if categoria:
            qs = qs.filter(categoria__nombre__icontains=categoria)
        return qs


class ProductoDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/productos/<id>/
    Detalle completo de un producto.
    Permiso: público (no requiere token)
    """
    serializer_class   = ProductoDetailSerializer
    permission_classes = [AllowAny]
    queryset           = Producto.objects.filter(activo=True).select_related('categoria')


class RegistroAPIView(generics.CreateAPIView):
    """
    POST /api/registro/
    Crea un nuevo usuario.
    Permiso: público
    """
    serializer_class   = RegistroSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'mensaje': f'Usuario "{user.username}" creado correctamente.'},
            status=status.HTTP_201_CREATED
        )


class PerfilAPIView(APIView):
    """
    GET /api/perfil/
    Devuelve el perfil del usuario autenticado.
    Permiso: requiere JWT
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            perfil = request.user.perfil
            serializer = PerfilSerializer(perfil)
            return Response(serializer.data)
        except Exception:
            return Response(
                {'error': 'El usuario no tiene perfil creado.'},
                status=status.HTTP_404_NOT_FOUND
            )


class CarritoAPIView(APIView):
    """
    GET /api/carrito/
    Devuelve el carrito activo del usuario autenticado.
    Permiso: requiere JWT
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carrito, _ = Carrito.objects.get_or_create(
            usuario=request.user, activo=True
        )
        serializer = CarritoSerializer(carrito)
        return Response(serializer.data)


# ──────────────────────────────────────────────────────────────────────────────
# APIs EXTERNAS CONSUMIDAS
# ──────────────────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def juegos_freetogame(request):
    """
    GET /api/juegos-externos/
    Consume FreeToGame API y devuelve juegos gratuitos.
    Parámetro opcional: ?genero=shooter
    Documentación: https://www.freetogame.com/api-doc
    """
    genero = request.query_params.get('genero', '')
    url    = 'https://www.freetogame.com/api/games'
    params = {}
    if genero:
        params['genre'] = genero

    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        datos = resp.json()

        juegos = [
            {
                'id':            j.get('id'),
                'titulo':        j.get('title'),
                'genero':        j.get('genre'),
                'plataforma':    j.get('platform'),
                'imagen':        j.get('thumbnail'),
                'url':           j.get('game_url'),
                'publicador':    j.get('publisher'),
                'desarrollador': j.get('developer'),
            }
            for j in datos[:20]
        ]
        return Response({'fuente': 'FreeToGame', 'total': len(juegos), 'juegos': juegos})

    except requests.exceptions.Timeout:
        return Response(
            {'error': 'La API de FreeToGame no respondió a tiempo.'},
            status=status.HTTP_504_GATEWAY_TIMEOUT
        )
    except requests.exceptions.RequestException as e:
        return Response(
            {'error': f'Error al conectar con FreeToGame: {str(e)}'},
            status=status.HTTP_502_BAD_GATEWAY
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def juegos_rawg(request):
    """
    GET /api/juegos-rawg/
    Consume RAWG API y devuelve videojuegos con metadata rica.
    Parámetro opcional: ?buscar=zelda  o  ?genero=action
    Documentación: https://rawg.io/apidocs
    """
    buscar = request.query_params.get('buscar', '')
    genero = request.query_params.get('genero', '')

    url    = 'https://api.rawg.io/api/games'
    params = {
        'page_size': 10,
        'key': os.environ.get('RAWG_API_KEY', 'a8e406f98b174c8b884e103c157558a5'),
    }
    if buscar:
        params['search'] = buscar
    if genero:
        params['genres'] = genero

    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        datos = resp.json()

        juegos = [
            {
                'id':          j.get('id'),
                'titulo':      j.get('name'),
                'lanzamiento': j.get('released'),
                'rating':      j.get('rating'),
                'imagen':      j.get('background_image'),
                'generos':     [g['name'] for g in j.get('genres', [])],
                'plataformas': [p['platform']['name'] for p in j.get('platforms', [])],
            }
            for j in datos.get('results', [])
        ]
        return Response({'fuente': 'RAWG', 'total': len(juegos), 'juegos': juegos})

    except requests.exceptions.Timeout:
        return Response(
            {'error': 'RAWG API no respondió a tiempo.'},
            status=status.HTTP_504_GATEWAY_TIMEOUT
        )
    except requests.exceptions.RequestException as e:
        return Response(
            {'error': f'Error al conectar con RAWG: {str(e)}'},
            status=status.HTTP_502_BAD_GATEWAY
        )