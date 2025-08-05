import os
from django.conf import settings
from django.shortcuts import render

def home(request):
    print("STATICFILES_DIRS:", settings.STATICFILES_DIRS)
    print("STATIC_URL:", settings.STATIC_URL)
    
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    return render(request, 'book.html')
