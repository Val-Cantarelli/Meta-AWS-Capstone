#!/bin/bash
export DJANGO_SETTINGS_MODULE=LittleLemon.LittleLemon.settings.local

# Activate virtual environment if not already active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    source .venv/bin/activate
fi

python manage.py "$@"
