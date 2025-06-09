from django.contrib import messages

import requests
from django.shortcuts import render
from urllib.parse import urlparse, parse_qs
from django.conf import settings

def menu(request):
    page = request.GET.get('page')
    if page and page != "1":
        previous_page = None
        api_url = f"{settings.API_BASE_URL}/api/menu-items?page={page}"
    else:
        api_url = f"{settings.API_BASE_URL}/api/menu-items"

    response = requests.get(api_url)
    print("Status:", response.status_code)
    print("Content:", response.text)

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
        if previous_page is None:
            previous_page = "1"

    context = {
        'items': items,
        'next_page': next_page,
        'previous_page': previous_page,
    }

    return render(request, 'menu.html', context)