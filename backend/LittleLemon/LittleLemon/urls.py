
from django.contrib import admin
from django.urls import path,include
from LittleLemonAPI.views import health_check

urlpatterns = [
    path('', health_check),
    path('admin/', admin.site.urls),
    path('api/', include('LittleLemonAPI.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls')), 
    #path('auth/', include('djoser.urls.authtoken')),
    
]
'''

Registro de usuário: /auth/users/
Login (JWT): /auth/jwt/create/
Refresh de token JWT: /auth/jwt/refresh/
Reset de senha: /auth/password/reset/

Criação de Usuário POST /auth/users/


'''