#!/bin/bash
unset DJANGO_ENV
export DJANGO_SETTINGS_MODULE=core.settings.local
export API_BASE_URL=https://6qpkzrhv4c.execute-api.us-east-1.amazonaws.com/v1


python manage.py runserver