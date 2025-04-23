from decouple import config

ENV = config("DJANGO_ENV", default="local")

if ENV == "production":
    from .production import *
else:
    from .local import *