import requests
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings


def autenticacion(request):
    username = settings.USUARIO
    password = settings.CONTRASEÑA

    response = requests.post('https://electroaires.herokuapp.com/api/token/', data={'username': username, 'password': password})

    if response.status_code == 200:
        token = response.json().get('access')
        headers = {
            'Authorization': 'Bearer ' + str(token),
        }
        return headers
    else:
        print(f'ERROR DE API ACCES -> {response.status_code}')
        return False