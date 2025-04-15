import time
import json
import requests
import os

TOKEN_FILE = "tokens.json"

# Se a variável de ambiente DJANGO_ENV for 'local', usa a URL local correta (porta 8001)
if os.getenv("DJANGO_ENV") == "local":
    BASE_URL = "http://127.0.0.1:8001"  # Backend Django local
else:
    BASE_URL = "https://xy3r212g98.execute-api.us-east-1.amazonaws.com/dev"  # Produção

session = requests.Session()  

def save_tokens(access, refresh):
    """It saves token in a file"""
    with open(TOKEN_FILE, "w") as f:
        json.dump({"access": access, "refresh": refresh}, f)

def load_tokens():
    """Load the token"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None

def login():
    """Faz login e armazena os tokens"""
    print("Executando login (isso só deve aparecer se o token não for renovado)")

    credentials = {"username": "test1", "password": "CasaAzul12"}  
    response = session.post(f"{BASE_URL}/auth/jwt/create/", json=credentials)

    print(f"Login response status: {response.status_code}")  
    print(f"Login response text: {response.text}")  

    if response.status_code == 200:
        try:
            tokens = response.json()  
            session.headers.update({"Authorization": f"Bearer {tokens['access']}"} )  
            save_tokens(tokens["access"], tokens["refresh"])  
            print("Login successful!")
            return True
        except Exception as e:
            print(f"Error saving the token: {e}")
            return False
    else:
        try:
            print("Login failed!", response.json())  
        except requests.exceptions.JSONDecodeError:
            print("Login failed! Answer from the server is not a valid JSON:", response.text)
        return False

def refresh_token():
    """renews the access token using refresh token"""
    tokens = load_tokens()
    if not tokens or "refresh" not in tokens:
        print("Refresh token not found. Login again")
        return False

    refresh_token = tokens["refresh"]
    response = session.post(f"{BASE_URL}/auth/jwt/refresh/", json={"refresh": refresh_token})

    print(f"Refresh response status: {response.status_code}")
    print(f"Refresh response text: {response.text}")

    if response.status_code == 200:
        try:
            new_access_token = response.json()["access"]
            session.headers.update({"Authorization": f"Bearer {new_access_token}"} )  
            save_tokens(new_access_token, refresh_token)  # 🔥 Atualiza o access token no arquivo
            print("New access token obtained successfully!")
            return True
        except Exception as e:
            print(f"Token was not saved: {e}")
            return False
    else:
        print("Refresh token expired. User needs to log in again.")
        os.remove(TOKEN_FILE)  # 🔥 Apaga os tokens antigos
        return False

def request_with_refresh(url, method="GET", data=None):
    """New request. Renews token - if necessary"""
    
    tokens = load_tokens()
    if not tokens or "access" not in tokens:
        print("Token not found! Login...")
        if not login():
            print("Login Error")
            return None

    session.headers.update({"Authorization": f"Bearer {tokens['access']}"} )  
    response = session.request(method, f"{BASE_URL}{url}", json=data)

    if response.status_code == 401:  # Token expirado ou inválido
        print("Access token expired. Trying to refresh...")
        if refresh_token():  # Se o refresh funcionar, tenta novamente a requisição
            tokens = load_tokens()
            session.headers.update({"Authorization": f"Bearer {tokens['access']}"} )  
            response = session.request(method, f"{BASE_URL}{url}", json=data)
        else:
            print("Re-authentication required.")
            if login():  # Força login novamente
                tokens = load_tokens()
                session.headers.update({"Authorization": f"Bearer {tokens['access']}"} )  
                response = session.request(method, f"{BASE_URL}{url}", json=data)

    return response

# Agora fazemos um teste contínuo por 5 minutos
if not load_tokens():
    login()  # Só faz login se não houver tokens salvos

for i in range(5):  #  Testa por 5 rodadas (a cada 30 segundos)
    print(f"\n Tentativa {i+1} de requisição...")
    response = request_with_refresh("/api/menu-items/")
    if response:
        print(response.status_code, response.json())
    else:
        print("Error")

    time.sleep(30)  #  Espera 30 segundos entre as requisições
