"""
Configuration for development. Take care of env.json in project root folder.
"""
import json
import sentry_sdk
from os import environ, path
from django.core.exceptions import ImproperlyConfigured
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


CURRENT_ENVIRONMENT = 'local'

SECRET_LIST = {}

try:
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url="https://learning2.vault.azure.net/", credential=credential)
    
    SECRET_LIST['django-secret'] = client.get_secret('django-secret').value
    SECRET_LIST['sentry-key'] = client.get_secret('sentry-key').value
    SECRET_LIST['postgres-user'] = client.get_secret('postgres-user').value
    SECRET_LIST['postgres-key'] = client.get_secret('postgres-pass').value
    SECRET_LIST['postgres-host'] = client.get_secret('postgres-host').value
    SECRET_LIST['postgres-name'] = client.get_secret('postgres-name').value
    SECRET_LIST['gremlin-key'] = client.get_secret('gremlin-pass').value
    SECRET_LIST['gremlin-user'] = client.get_secret('gremlin-username').value

    print(DEBUG)
  
except Exception as e:
    raise ImproperlyConfigured("KeyVault issue")

def _before_send(event,hint):
    if DEBUG is True:
        print(event)
        return None
    else:
        return event
  

sentry_sdk.init(
    dsn=SECRET_LIST['sentry-key'],
    integrations=[DjangoIntegration()],
    attach_stacktrace=True
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_LIST['django-secret']
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
CORE_ORIGIN_WHITELIST = ["*"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': SECRET_LIST['postgres-name'],
        'USER': SECRET_LIST['postgres-user'],
        'PASSWORD': SECRET_LIST['postgres-key'],
        'HOST': SECRET_LIST['postgres-host'],
        'PORT': '5432'
    }
}


