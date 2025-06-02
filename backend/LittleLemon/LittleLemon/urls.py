
from django.contrib import admin
from django.urls import path,include
from LittleLemon.LittleLemonAPI.views import health_check

urlpatterns = [
    path('health', health_check),
    path('admin/', admin.site.urls),
    path('api/', include('LittleLemon.LittleLemonAPI.urls')),
    path('auth/', include('djoser.urls')), 
    path('auth/', include('djoser.urls.jwt')),
    
]
