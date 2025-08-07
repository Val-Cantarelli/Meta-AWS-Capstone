from django.urls import path
from ui_app.views.base_views import  home, about, book, health
from ui_app.views.auth_views import login_view,signup_view
from ui_app.views.menu_views import menu

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('menu-items/', menu, name='menu'),
    path('book/', book, name='book'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('health/', health, name='health'),
]
