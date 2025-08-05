#!/bin/bash
DJANGO_ENV=production
API_BASE_URL=Ajustar

python manage.py collectstatic --noinput
python manage.py runserver