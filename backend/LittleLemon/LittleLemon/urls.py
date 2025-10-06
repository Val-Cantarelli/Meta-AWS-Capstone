
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
from LittleLemon.LittleLemonAPI.views import health_check
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

def api_redirect(request):
    """Redirect /api to /api/ for better UX while maintaining trailing_slash=False design"""
    return redirect('/api/')

urlpatterns = [
    path('health', health_check),
    path('admin/', admin.site.urls),
    path('api', api_redirect),  # Manual redirect for /api -> /api/
    path('api/', include('LittleLemon.LittleLemonAPI.urls')),
    path('auth/', include('djoser.urls')), 
    path('auth/', include('djoser.urls.jwt')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
]
