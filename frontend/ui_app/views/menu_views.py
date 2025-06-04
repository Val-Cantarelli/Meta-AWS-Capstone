from django.contrib import messages

import requests
import logging
from django.shortcuts import render, redirect
from urllib.parse import urlparse, parse_qs
from django.conf import settings
from ui_app.api.auth_utils import refresh_access_token

def menu(request):
    page = request.GET.get('page')
    if page and page != "1":
        api_url = f"{settings.API_BASE_URL}/api/menu-items?page={page}"
    else:
        api_url = f"{settings.API_BASE_URL}/api/menu-items"

    token = request.session.get('access')
    if not token:
        messages.warning(request, 'You need to log in first.')
        logging.warning("Access token not found in session.")
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(api_url, headers=headers)
    print("Status:", response.status_code)
    print("Content:", response.text)
    
    if response.status_code in [401,403]:
        new_access = refresh_access_token(request)
        if new_access:
            headers['Authorization'] = f'Bearer {new_access}'
            response = requests.get(api_url, headers=headers)
        if response.status_code in [401, 403]:
            request.session.flush()
            messages.warning(request, 'Session expired. Please log in again.')
            return redirect('login')
    try:
        data = response.json()
    except Exception as e:
        print("Error decoding JSON:", e)
        print("Raw response:", response.text)
        messages.error(request, "Error retrieving the items")
        return render(request, 'menu.html', {'items': [], 'next_page': None, 'previous_page': None})

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
    print("API URL:", api_url)

    return render(request, 'menu.html', context)
