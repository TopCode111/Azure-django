from .views import auth, complete, validate_token
from django.conf.urls import url


urlpatterns = [
    url(r'^login/$', auth, name='azure_login'),
    url(r'^complete/$', complete, name='azure_complete'),
    url(r'^validate_token/$', validate_token, name='azure_validate_token'),
]