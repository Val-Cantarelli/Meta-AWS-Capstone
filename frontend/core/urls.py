from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ui_app.urls')),
]

if settings.DEBUG:
    # Serve arquivos da pasta de desenvolvimento (ui_app/static/)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "ui_app" / "static")
else:
    # Serve arquivos já coletados em STATIC_ROOT (staticfiles/)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)