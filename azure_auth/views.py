from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from jwt import DecodeError, ExpiredSignature, decode as jwt_decode
from jwt.utils import base64url_decode
import json
from requests import request as _request
from jwt.algorithms import RSAAlgorithm
from cryptography.hazmat.primitives import serialization
from django.shortcuts import render


@never_cache
def auth(request):

    LOGIN_BASE_URL = 'https://{tenant_name}.b2clogin.com/{tenant_name}.onmicrosoft.com'.format(
        tenant_name=settings.TENANT_NAME)
    AUTHORIZATION_URL = '{base_url}/oauth2/v2.0/authorize'.format(
        base_url=LOGIN_BASE_URL)
    OPENID_CONFIGURATION_URL = '{auth_url}?p={policy}&client_id={client_id}&nonce=defaultNonce&redirect_uri={redirect_uri}&scope=openid&response_type=id_token&prompt=login'.format(
        auth_url=AUTHORIZATION_URL, policy=settings.POLICY, client_id=settings.CLIENT_ID, redirect_uri=settings.REDIRECT_URI)

    return HttpResponseRedirect(OPENID_CONFIGURATION_URL)


@never_cache
@csrf_exempt
def complete(request):
    return render(request, 'loading.html', {})


@never_cache
@csrf_exempt
def validate_token(request):
    BASE_URL = 'https://login.microsoftonline.com/{tenant_id}'.format(
        tenant_id=settings.TENANT_ID)
    JWKS_URL = '{base_url}/discovery/v2.0/keys?p={policy}'.format(
        base_url=BASE_URL, policy=settings.POLICY)

    if request.GET.get('error'):
        if 'The user has cancelled entering self-asserted information.' in request.GET.get('error_description'):
            return HttpResponseRedirect('/azure_auth/login/')
        else:
            return HttpResponse('failure, ' + str(reques.GET.get('error_description')))
    else:
        id_token = request.GET['id_token']
        jwt_header_json = base64url_decode(id_token.split('.')[0])
        jwt_header = json.loads(jwt_header_json.decode('ascii'))
        resp = _request(url=JWKS_URL, method="GET")
        pub_key_val = ''
        for key in resp.json()['keys']:
            if key['kid'] == jwt_header['kid']:
                pub_key = RSAAlgorithm.from_jwk(json.dumps(key))
                pub_key_val = pub_key.public_bytes(
                    encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        try:
            user_info = jwt_decode(
                id_token, key=pub_key_val, algorithms=jwt_header['alg'], audience=settings.CLIENT_ID, leeway=0)
            return HttpResponse('Login success, ' + json.dumps(user_info))
        except (DecodeError, ExpiredSignature) as error:
            return HttpResponse('failure, ' + str(error))
        except Exception as e:
            return HttpResponse('failure, ' + str(e))
