#!/bin/bash
DJANGO_ENV=production
API_BASE_URL=https://xy3r212g98.execute-api.us-east-1.amazonaws.com/dev

python manage.py collectstatic --noinput
python manage.py runserver