import re
import requests


def validar_placa(placa):
    patron_placa = r'^[A-Z]{3}\d{3}$'
    if not re.match(patron_placa, placa):
        return False
    ultimo_digito = int(placa[-1])
    if ultimo_digito == 0 or ultimo_digito == 1:
        return False

    if placa == 'CD' or placa == 'CC' or placa == 'DT' or placa == 'AT':
        return False

    if placa.startswith('PR') or placa.startswith('PT'):
        return False
    if placa.startswith('AL'):
        return False

    if placa.startswith('TC'):
        return False

    return True


def validar_cedula(cedula):
    if len(cedula) >= 6 and len(cedula) <= 10 and cedula.isdigit():
        return True
    elif cedula == ' ':
        return False
    else:
        return False


def obtener_servicios_activos():
    url = 'https://api-electroaires-30a0049f64a4.herokuapp.com/servicios/'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        servicios = []
        for item in data:
            servicio_id = item['id']
            vehiculo = item['s_vehiculo']
            estado = item['estado']
            if estado:
                servicios.append(
                    {'id': servicio_id, 'vehiculo': vehiculo, 'estado': 'ACTIVO'})
        return servicios
    else:
        print('Error al obtener los servicios activos')
        return []
