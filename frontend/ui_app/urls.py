from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu-items/', views.menu, name='menu'),
    path('book/', views.book, name='book'),
    path('login/', views.login, name='login'),
    
]