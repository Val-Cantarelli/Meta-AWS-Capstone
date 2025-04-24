import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from ui_app.api.auth_utils import login_user 

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

    api_url = f"{settings.API_BASE_URL}/auth/jwt/create/"
    response = requests.post(api_url, json={"username": username, "password": password})

    if response.status_code == 200:
        data = response.json()        
        
        request.session["username"] = username
        request.session["access"] = data.get("access")
        request.session["refresh"] = data.get("refresh")
        request.session.modified = True
        print("Token salvo:", request.session.get("access"))
        
        messages.success(request, 'Login successful!')
        return redirect('menu') 

    else:
        print("Login error:", response.status_code, response.text)
        messages.error(request, 'Invalid username or password.')
        return render(request, 'login_signup.html')

def custom_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email'] 
        password = request.POST['password']
        re_password = request.POST['re_password']
        
        if password != re_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'login_signup.html')

        api_url = f"{settings.API_BASE_URL}/auth/users/"
        headers = {
            "Content-Type": "application/json",
            "Host": "xy3r212g98.execute-api.us-east-1.amazonaws.com"
        }
        response = requests.post(api_url, json={
            'username': username, 
            'email': email, 
            'password': password,
            're_password': re_password,
        },headers=headers)

        if response.status_code == 201:
            login_response = requests.post(
                f"{settings.API_BASE_URL}/auth/jwt/create/",
                json={'username': username, 'password': password}
            )

            if login_response.status_code == 200:
                data = login_response.json()
                request.session["access"] = data.get("access")
                request.session["refresh"] = data.get("refresh")
                request.session["username"] = username

                messages.success(request, 'Account created and logged in successfully!')
                return redirect('menu')
            else:
                messages.success(request, 'Account created, but automatic login failed.')
                return redirect('auth_page')

        else:
            print("Erro no signup:", response.status_code, response.text)
            messages.error(request, 'Error during signup. Please try again.')
            return render(request, 'login_signup.html')
    
    return render(request, 'login_signup.html')