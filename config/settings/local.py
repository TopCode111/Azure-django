"""
Configuration for development. Take care of env.json in project root folder.
"""
import json
import sentry_sdk
from os import environ, path
from django.core.exceptions import ImproperlyConfigured
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *


CURRENT_ENVIRONMENT = 'local'

ENV_FILE = path.join(path.dirname(BASE_DIR), 'local_env.json')
if not path.exists(ENV_FILE):
    raise ImproperlyConfigured("No local environment file was found in\
        directory: {0}".format(BASE_DIR))
with open(ENV_FILE) as data_file:
    ENV_JSON = json.load(data_file)

if not ENV_JSON:
    raise ImproperlyConfigured("No environment variables were found")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_JSON.get('DJANGO_SECRET_KEY', None)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
CORE_ORIGIN_WHITELIST = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ENV_JSON.get('DATABASE_NAME'),
        'USER': ENV_JSON.get('DATABASE_USER'),
        'PASSWORD': ENV_JSON.get('DATABASE_PW'),
        'HOST': ENV_JSON.get('DATABASE_HOST'),
        'PORT': '5432',
    }
}

sentry_sdk.init(
    dsn=ENV_JSON.get('DSN'),
    integrations=[DjangoIntegration()]
)
