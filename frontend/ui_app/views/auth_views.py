import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from ui_app.api.auth_utils import login_user  # 🔥 Importa do `auth_utils.py`

def auth_page(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST and 'email' not in request.POST:
            return custom_login(request)
        elif 'username' in request.POST and 'email' in request.POST:
            return custom_signup(request)
    
    return render(request, 'login_signup.html')

def custom_login(request):
    username = request.POST['username']
    password = request.POST['password']

    if login_user(request, username, password):
        messages.success(request, 'Login successful!')
        return redirect('home')
    else:
        messages.error(request, 'Invalid username or password.')
        return render(request, 'login_signup.html')

def custom_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email'] 
        password = request.POST['password']

        api_url = f"{settings.API_BASE_URL}/auth/users/"
        response = requests.post(api_url, json={'username': username, 'email': email, 'password': password})

        if response.status_code == 201:
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login_signup')
        else:
            messages.error(request, 'Error during signup. Please try again.')
            return render(request, 'login_signup.html')

    return render(request, 'login_signup.html')
