#!/bin/bash
unset DJANGO_ENV

API_BASE_URL=http://localhost:8000
python manage.py runserver