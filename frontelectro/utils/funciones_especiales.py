import re

def validar_placa(placa):
    # Patrón para validar la placa
    patron_placa = r'^[A-Z]{3}\d{3}$'

    # Verificar el formato de la placa
    if not re.match(patron_placa, placa):
        return False

    # Obtener el último dígito de la placa
    ultimo_digito = int(placa[-1])

    # Verificar restricciones según el último dígito
    if ultimo_digito == 0 or ultimo_digito == 1:
        return False

    # Placas especiales para vehículos oficiales o diplomáticos
    if placa == 'CD' or placa == 'CC' or placa == 'DT' or placa == 'AT':
        return False

    # Placas especiales para vehículos de pruebas
    if placa.startswith('PR') or placa.startswith('PT'):
        return False

    # Placas especiales para vehículos de alquiler
    if placa.startswith('AL'):
        return False

    # Placas especiales para vehículos de tránsito temporal
    if placa.startswith('TC'):
        return False

    # La placa es válida
    return True
