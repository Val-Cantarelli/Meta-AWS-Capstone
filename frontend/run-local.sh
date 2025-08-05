#!/bin/bash
unset DJANGO_ENV
export DJANGO_SETTINGS_MODULE=core.settings.local
export API_BASE_URL=http://localhost:8001

<<<<<<< HEAD
=======
API_BASE_URL=http://localhost:8000
>>>>>>> deploy-frontend
python manage.py runserver