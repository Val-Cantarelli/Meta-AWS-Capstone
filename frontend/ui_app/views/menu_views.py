from django.contrib import messages

import requests
import logging
from django.shortcuts import render, redirect
from urllib.parse import urlparse, parse_qs
from django.conf import settings

def menu(request):
    page = request.GET.get('page', 1)
    api_url = f"{settings.API_BASE_URL}/api/menu-items?page={page}"
    
    token = request.session.get('access') 
    headers = {'Authorization': f'Bearer {token}'} if token else {}

    response = requests.get(api_url, headers=headers)
    
    if response.status_code in [401,403]:
        request.session.flush()  
        messages.warning(request, 'Session expired.')
        return redirect('auth_page')

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
    

    print("Headers:", headers)
    print("Token:", token)
    print("URL:", api_url)
    print("Status:", response.status_code)
    print("JSON:", data)




    return render(request, 'menu.html', context)
