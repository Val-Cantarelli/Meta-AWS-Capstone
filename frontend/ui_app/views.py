import requests
import logging
from django.shortcuts import render
from urllib.parse import urlparse, parse_qs


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    return render(request, 'book.html')

def login(request):
    # render another page(signUp) if the customer is not registered
    return render(request, 'login.html')

def menu(request):
    page = request.GET.get('page', 1)
    base_api_url = "https://xy3r212g98.execute-api.us-east-1.amazonaws.com/dev/api/menu-items"
    api_url = f"{base_api_url}?page={page}"
    
    token = "edcbb7e26d742ea692704781d5889497fbf744ad"
    headers = {'Authorization': f'Token {token}'}
    
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
        
