#!/bin/bash
<<<<<<< HEAD
unset DJANGO_ENV
export DJANGO_SETTINGS_MODULE=core.settings.production
export API_BASE_URL=https://6qpkzrhv4c.execute-api.us-east-1.amazonaws.com/v1
=======
DJANGO_ENV=production
API_BASE_URL=https://littlelemon-env.eba-gpgijkvt.us-east-1.elasticbeanstalk.com
>>>>>>> deploy-frontend

python manage.py collectstatic --noinput
python manage.py runserver