import requests
import logging
from django.shortcuts import render, redirect
from urllib.parse import urlparse, parse_qs
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    return render(request, 'book.html')

def menu(request):
    page = request.GET.get('page', 1)
    base_api_url = "https://xy3r212g98.execute-api.us-east-1.amazonaws.com/dev/api/menu-items"
    api_url = f"{base_api_url}?page={page}"
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM5MzE2MTU1LCJpYXQiOjE3MzkzMTI1NTUsImp0aSI6ImFhZmJiYWU4ODBiNDQ5M2U5Y2VmNzdmNGVlMDY1MWIxIiwidXNlcl9pZCI6NH0.sBmN7vuFcVOCxoqlS21Zt7ggliWeRYFKEada81HVXm0"
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(api_url, headers=headers)
    data = response.json()
    
    items = data.get('results', [])
    
    next_page = None
    previous_page = None
    
    if data.get('next'):
        parsed_next = urlparse(data.get('next'))
        query_next = parse_qs(parsed_next.query)
        next_page = query_next.get('page', [None])[0]
    if data.get('previous'):
        parsed_prev = urlparse(data.get('previous'))
        query_prev = parse_qs(parsed_prev.query)
        previous_page = query_prev.get('page', [None])[0]
    
    context = {
        'items': items,
        'next_page': next_page,
        'previous_page': previous_page,
    }
    
    

    print("Status Code:", response.status_code)
    print("Resposta da API:", response.text)
    print("Page: ",response.url)
    logging.info("Status Code: %s", response.status_code)
    logging.info("Resposta da API: %s", response.text)
    if response.status_code == 401:
        print("Session expired!")
        return redirect('auth_page')
         
    
    if response.status_code == 200:
        try:
            data = response.json()  
            items = data.get('results', [])
        except ValueError as e:
            print("Erro ao decodificar JSON:", e)
            items = []
    else:
        items = []
         
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/menu_pagination.html', context)
    else:
        return render(request, 'menu.html', context)
        

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
    
    api_url = "https://xy3r212g98.execute-api.us-east-1.amazonaws.com/dev/auth/jwt/create/"
    response = requests.post(api_url, json={'username': username, 'password': password})
    
    if response.status_code == 200:
        
        tokens = response.json()
        access_token = tokens.get('access')  
        refresh_token = tokens.get('refresh')  
        
        request.session['access'] = access_token
        request.session['refresh'] = refresh_token
        
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

        # Faz a requisição para o endpoint de signup do Djoser
        api_url = "https://xy3r212g98.execute-api.us-east-1.amazonaws.com/dev/auth/users/"
        response = requests.post(api_url, json={
            'username': username,
            'email': email,
            'password': password
        })

        if response.status_code == 201:
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login_signup')
        else:
            messages.error(request, 'Error during signup. Please try again.')
            return render(request, 'login_signup.html')

    return render(request, 'login_signup.html')

'''
Resumo de como ficará a arquitetura de endpoints:
Cadastro de usuário: POST https://xy3r212g98.execute-api.us-east-1.amazonaws.com/dev/auth/users/
Login e JWT: POST https://xy3r212g98.execute-api.us-east-1.amazonaws.com/dev/auth/jwt/create/
Renovação de token: POST https://xy3r212g98.execute-api.us-east-1.amazonaws.com/dev/auth/jwt/refresh/


'''