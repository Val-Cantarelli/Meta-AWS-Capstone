from django.urls import path
from ui_app.views.base_views import home, about, book
from ui_app.views.auth_views import auth_page
from ui_app.views.menu_views import menu

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('menu-items/', menu, name='menu'),
    path('book/', book, name='book'),
    path('auth/', auth_page, name='auth_page'),
    
]
