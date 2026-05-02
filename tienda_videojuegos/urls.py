from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ── Admin de Django ───────────────────────────────────────────────
    path('admin/', admin.site.urls),

    # ── Rutas principales de la aplicación ───────────────────────────
    path('', include('core.urls')),

    # ── APIs REST con JWT (Semana 8) ──────────────────────────────────
    path('api/', include('core.api_urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)