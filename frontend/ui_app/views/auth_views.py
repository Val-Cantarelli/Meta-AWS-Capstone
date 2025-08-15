import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from ui_app.api.auth_utils import login_user 
from ui_app.forms import SignupForm
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator


def signup_view(request):
    form = SignupForm(request.POST or None)

    if request.method == "POST":
        if not form.is_valid():
            return render(request, "signup.html", {"form": form})

        data = form.cleaned_data
        api = settings.API_BASE_URL.rstrip('/')

        # cria usuário
        try:
            resp = requests.post(
                f"{api}/auth/users/",
                json={
                    "username": data["username"],
                    "email": data["email"],
                    "password": data["password"],
                    "re_password": data["re_password"],
                },
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=(3.05, 12),
            )
        except requests.RequestException as e:
            messages.error(request, f"Signup error: {e}")
            return render(request, "signup.html", {"form": form})

        if resp.status_code == 400:
            # injeta erros de validação da API no form
            try:
                errors = resp.json()
            except ValueError:
                errors = {"__all__": ["Unexpected error. Try again."]}
            for field, msgs in (errors or {}).items():
                msgs = msgs if isinstance(msgs, list) else [msgs]
                form.add_error(field if field in form.fields else None, msgs[0])
            return render(request, "signup.html", {"form": form})

        resp.raise_for_status()

        # login automático
        try:
            login_resp = requests.post(
                f"{api}/auth/jwt/create/",
                json={"username": data["username"], "password": data["password"]},
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=(3.05, 12),
            )
        except requests.RequestException as e:
            messages.error(request, f"Login after signup failed: {e}. Please log in manually.")
            return render(request, "signup.html", {"form": form})

        if login_resp.status_code != 200:
            messages.error(request, "Login after signup failed. Please try to log in manually.")
            return render(request, "signup.html", {"form": form})

        tokens = login_resp.json()
        request.session["access"] = tokens.get("access")
        request.session["refresh"] = tokens.get("refresh")
        request.session["username"] = data["username"]

        # detalhes opcionais do usuário
        try:
            me = requests.get(
                f"{api}/auth/users/me/",
                headers={"Authorization": f"Bearer {tokens.get('access')}", "Accept": "application/json"},
                timeout=(3.05, 12),
            )
            if me.status_code == 200:
                request.session["user_id"] = me.json().get("id")
        except requests.RequestException:
            pass

        messages.success(request, "Account created and logged in successfully!")
        return redirect("home")

    # GET
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        api_url = f"{settings.API_BASE_URL}/auth/jwt/create/"
        headers = {
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(
                api_url,
                json={'username': username, 'password': password},
                headers=headers,
                timeout=15,
            )
        except requests.RequestException as e:
            print("Login error:", e)
            messages.error(request, f"Login error: {e}")
            return render(request, 'login.html')

        if response.status_code == 200:
            data = response.json()
            request.session["access"] = data.get("access")
            request.session["refresh"] = data.get("refresh")
            request.session["username"] = username

            user_response = requests.get(
                f"{settings.API_BASE_URL}/auth/users/me/",
                headers={"Authorization": f"Bearer {data.get('access')}"},
                timeout=15,
            )
            if user_response.status_code == 200:
                user_data = user_response.json()
                request.session["user_id"] = user_data.get("id")

            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            # Try to extract error details
            try:
                err = response.json()
            except ValueError:
                err = {"detail": [response.text]}
            if isinstance(err, dict):
                for field, msgs in err.items():
                    if isinstance(msgs, list):
                        for m in msgs:
                            messages.error(request, f"{field}: {m}")
                    else:
                        messages.error(request, f"{field}: {msgs}")
            else:
                messages.error(request, str(err))

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