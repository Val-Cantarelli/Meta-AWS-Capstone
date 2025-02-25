import os

# If there is no django_ defined, assume: "local"
ENV = os.getenv("DJANGO_ENV", "local")

if ENV == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LittleLemon.settings.production")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LittleLemon.settings.local")