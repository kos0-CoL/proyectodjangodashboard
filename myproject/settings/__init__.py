"""
Selector de settings por variable de entorno DJANGO_SETTINGS_MODULE.
Por defecto usa development.
"""
import os

settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'myproject.settings.development')

# Esto permite: python manage.py runserver --settings=myproject.settings.production
# O export DJANGO_SETTINGS_MODULE=myproject.settings.production