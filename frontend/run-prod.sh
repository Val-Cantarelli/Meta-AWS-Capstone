#!/bin/bash
export DJANGO_ENV=production
export DJANGO_SETTINGS_MODULE=core.settings.production
export API_BASE_URL=https://6qpkzrhv4c.execute-api.us-east-1.amazonaws.com/v1
python manage.py collectstatic --noinput
python manage.py runserver