# scripts/jwt_client.py

import os
import time
import json
import requests

TOKEN_FILE = "tokens.json"

class JWTClient:
    def __init__(self, env, username, password):
        self.session = requests.Session()
        self.username = username
        self.password = password

        if env == "local":
            self.base_url = "http://127.0.0.1:8001"
        else:
            self.base_url = "https://xy3r212g98.execute-api.us-east-1.amazonaws.com/dev"

    def save_tokens(self, access, refresh):
        with open(TOKEN_FILE, "w") as f:
            json.dump({"access": access, "refresh": refresh}, f)

    def load_tokens(self):
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                return json.load(f)
        return None

    def login(self):
        print("Login...")
        credentials = {"username": self.username, "password": self.password}
        response = self.session.post(f"{self.base_url}/auth/jwt/create/", json=credentials)

        if response.status_code == 200:
            tokens = response.json()
            self.session.headers.update({"Authorization": f"Bearer {tokens['access']}"})
            self.save_tokens(tokens["access"], tokens["refresh"])
            return True
        else:
            print("Login error:", response.text)
            return False

    def refresh_token(self):
        tokens = self.load_tokens()
        if not tokens or "refresh" not in tokens:
            print("Refresh token not found.")
            return False

        response = self.session.post(f"{self.base_url}/auth/jwt/refresh/", json={"refresh": tokens["refresh"]})
        if response.status_code == 200:
            new_access = response.json()["access"]
            self.session.headers.update({"Authorization": f"Bearer {new_access}"})
            self.save_tokens(new_access, tokens["refresh"])
            return True
        else:
            print("Renew token failed:", response.text)
            os.remove(TOKEN_FILE)
            return False

    def request_with_refresh(self, url, method="GET", data=None):
        tokens = self.load_tokens()
        if not tokens or "access" not in tokens:
            if not self.login():
                return None

        self.session.headers.update({"Authorization": f"Bearer {tokens['access']}"})
        response = self.session.request(method, f"{self.base_url}{url}", json=data)

        if response.status_code == 401:
            print("Access token expired. Trying refressh...")
            if self.refresh_token():
                tokens = self.load_tokens()
                self.session.headers.update({"Authorization": f"Bearer {tokens['access']}"})
                response = self.session.request(method, f"{self.base_url}{url}", json=data)
            else:
                print("Login again...")
                if self.login():
                    tokens = self.load_tokens()
                    self.session.headers.update({"Authorization": f"Bearer {tokens['access']}"})
                    response = self.session.request(method, f"{self.base_url}{url}", json=data)

        return response
