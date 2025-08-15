from django.contrib import messages

import requests
from django.shortcuts import render
from urllib.parse import urlparse, parse_qs
from django.conf import settings


def _extract_page_param(url: str, key: str = "page"):
    try:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        return query.get(key, [None])[0]
    except Exception:
        return None


def menu(request):
    page = request.GET.get('page')

    api_base = settings.API_BASE_URL.rstrip('/')
    endpoint = f"{api_base}/api/menu-items"  # no trailing slash to match APPEND_SLASH=False

    params = {}
    if page and page != "1":
        params['page'] = page

    try:
        response = requests.get(
            endpoint,
            params=params,
            headers={"Accept": "application/json"},
            timeout=12,
        )
    except requests.RequestException:
        messages.error(request, "Error retrieving the items")
        return render(request, 'menu.html', {'items': [], 'next_page': None, 'previous_page': None})

    try:
        data = response.json()
    except ValueError:
        messages.error(request, "Error decoding server response")
        return render(request, 'menu.html', {'items': [], 'next_page': None, 'previous_page': None})

    items = []
    next_page = None
    previous_page = None

    # Support both paginated (DRF PageNumberPagination) and plain list responses
    if isinstance(data, list):
        items = data
    else:
        items = data.get('results') or data.get('items') or []

        next_url = data.get('next')
        prev_url = data.get('previous')

        next_page = _extract_page_param(next_url) if next_url else None
        previous_page = _extract_page_param(prev_url) if prev_url else None

        # Fallback if the API uses offset pagination
        if not next_page and next_url:
            next_page = _extract_page_param(next_url, key='offset')
        if not previous_page and prev_url:
            previous_page = _extract_page_param(prev_url, key='offset')

    # Extra fallback: if API didn’t send `previous` but URL has page>1, compute previous
    if (not previous_page) and page and page.isdigit() and int(page) > 1:
        previous_page = str(int(page) - 1)

    context = {
        'items': items,
        'next_page': next_page,
        'previous_page': previous_page,
    }

    return render(request, 'menu.html', context)