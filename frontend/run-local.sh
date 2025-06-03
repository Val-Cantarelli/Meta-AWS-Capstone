#!/bin/bash
unset DJANGO_ENV
export DJANGO_SETTINGS_MODULE=core.settings.local
export API_BASE_URL=http://localhost:8000

python manage.py runserver