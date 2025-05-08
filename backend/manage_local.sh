#!/bin/bash
export DJANGO_SETTINGS_MODULE=LittleLemon.LittleLemon.settings.local
python manage.py "$@"

# Remember to run: ./manage_dev.sh runserver