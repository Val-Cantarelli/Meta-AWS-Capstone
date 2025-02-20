import requests
from django.conf import settings

def login_user(request, username, password):
    """Autentica o usuário e armazena os tokens."""
    api_url = f"{settings.API_BASE_URL}/auth/jwt/create/"
    response = requests.post(api_url, json={'username': username, 'password': password})

    if response.status_code == 200:
        tokens = response.json()
        request.session['access'] = tokens.get('access')
        request.session['refresh'] = tokens.get('refresh')
        return True
    return False

def refresh_access_token(request):
    """Tenta renovar o token de acesso usando o refresh token."""
    refresh_token = request.session.get('refresh')
    if not refresh_token:
        return None

    api_url = f"{settings.API_BASE_URL}/auth/jwt/refresh/"
    response = requests.post(api_url, json={'refresh': refresh_token})

    if response.status_code == 200:
        tokens = response.json()
        request.session['access'] = tokens.get('access')
        return tokens.get('access')
    return None
