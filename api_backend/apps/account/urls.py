from django.urls import include, path
from rest_framework_nested import routers

from .import views as v

router = routers.SimpleRouter(trailing_slash=False)
