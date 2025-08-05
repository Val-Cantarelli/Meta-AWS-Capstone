#!/bin/bash
DJANGO_ENV=production
API_BASE_URL=https://littlelemon-env.eba-gpgijkvt.us-east-1.elasticbeanstalk.com

python manage.py collectstatic --noinput
python manage.py runserver