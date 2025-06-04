import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from ui_app.api.auth_utils import login_user 

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email'] 
        password = request.POST['password']
        re_password = request.POST['re_password']
        
        if password != re_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        api_url = f"{settings.API_BASE_URL}/auth/users/"
        headers = {
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(api_url, json={
                'username': username,
                'email': email,
                'password': password,
                're_password': re_password
            }, headers=headers)
            response.raise_for_status()
            
        except Exception as e:
            print("Error while creating user:", e)
            print("Response:", response.text)
            messages.error(request, f"Signup error: {e}")
            return render(request, 'signup.html')

        if response.status_code == 201:
            # Automatic login after signup
            login_response = requests.post(
                f"{settings.API_BASE_URL}/auth/jwt/create/",
                json={'username': username, 'password': password}
            )
            if login_response.status_code != 200:
                messages.error(request, 'Login after signup failed. Please try again.')
                return render(request, 'signup.html')
            data = login_response.json()
            request.session["access"] = data.get("access")
            request.session["refresh"] = data.get("refresh")
            request.session["username"] = username
           
            user_response = requests.get(
                f"{settings.API_BASE_URL}/auth/users/me/",
                headers={"Authorization": f"Bearer {data.get('access')}"}
            )
            if user_response.status_code == 200:
                user_data = user_response.json()
                request.session["user_id"] = user_data["id"]
            else:
                messages.error(request, 'Failed to fetch user details after signup.')
                return render(request, 'signup.html')
            messages.success(request, 'Account created and logged in successfully!')
            return redirect('menu')
        else:
            print("Erro no signup:", response.status_code, response.text)
            messages.error(request, 'Error during signup. Please try again.')
            return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        api_url = f"{settings.API_BASE_URL}/auth/jwt/create/"
        headers = {
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(api_url, json={
                'username': username,
                'password': password
            }, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print("Erro ao fazer login:", e)
            print("Resposta:", response.text)
            messages.error(request, f"Login error: {e}")
            return render(request, 'login.html')

        if response.status_code == 200:
            data = response.json()
            request.session["access"] = data.get("access")
            request.session["refresh"] = data.get("refresh")
            request.session["username"] = username

            user_response = requests.get(
                f"{settings.API_BASE_URL}/auth/users/me/",
                headers={"Authorization": f"Bearer {data.get('access')}"}
            )
            if user_response.status_code == 200:
                user_data = user_response.json()
                request.session["user_id"] = user_data.get("id")

            messages.success(request, 'Logged in successfully!')
            return redirect('menu')

    return render(request, 'login.html')




def refresh_access_token(request):
    refresh_token = request.session.get("refresh")
    if not refresh_token:
        return None
    refresh_url = f"{settings.API_BASE_URL}/auth/jwt/refresh/"
    response = requests.post(refresh_url, json={"refresh": refresh_token})
    if response.status_code == 200:
        new_access = response.json().get("access")
        request.session["access"] = new_access
        return new_access
    return None