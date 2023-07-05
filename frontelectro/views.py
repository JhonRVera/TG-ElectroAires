import requests
import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from frontelectro.utils.funciones_especiales import validar_placa, obtener_servicios_activos, validar_cedula
from frontelectro.utils.autenticacion import autenticacion


# Create your views here.
def home(request):
    return render(request, 'home/home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('correo')
        password = request.POST.get('contrasena')
        data = {
            'correo': username,
            'contrasena': password
        }
        url = 'https://electroaires.herokuapp.com/usuarios/verificacion/'
        response = requests.post(url, data=data)

        if response.status_code == 200:
            return redirect('dashboard')
        else:
            return render(request, 'home/login.html', {'error_message': 'Credenciales inválidas'})

    return render(request, 'home/login.html')


def crear_cliente(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        if validar_cedula(cedula):
            cedula = request.POST.get('cedula')
            nombre = request.POST.get('nombre')
            celular = request.POST.get('celular')
            data_nuevo = {
                'cedula': cedula,
                'nombre': nombre,
                'celular': celular
            }
            url = 'https://electroaires.herokuapp.com/clientes/'
            response = requests.post(
                url, data=data_nuevo, headers=autenticacion(request))

            if response.status_code == 201:
                messages.success(request, 'Cliente creado correctamente')
            else:
                messages.error(
                    request, f'Error al crear el cliente. Código de respuesta: {response.status_code}')
        elif cedula is None:
            messages.error(request, ' ')
    return redirect('dashboard')


def dashboard(request):
    servicios = obtener_servicios_activos()
    if request.method == 'POST':
        cedula = request.POST.get('cedula_clt')
        if validar_cedula(cedula):
            # Verificar cliente existente
            url = f'https://electroaires.herokuapp.com/clientes/{cedula}/'
            response = requests.get(url, headers=autenticacion(request))
            data_json = {}
            try:
                data_json = response.json()
            except json.JSONDecodeError:
                pass
            if 'detail' in data_json and data_json['detail'] == 'Not found.':
                return render(request, 'dashboard/dashboard.html', {'crear_cliente': True, 'servicios': servicios, 'mensaje': "Cliente no encontrado"})
            if response.status_code == 200:
                cedula = data_json.get('cedula')
                nombre = data_json.get('nombre')
                celular = data_json.get('celular')
                return render(request, 'dashboard/dashboard.html', {'cliente_encontrado': True, 'cedula': cedula, 'nombre': nombre, 'celular': celular, 'mostrar_data': True, 'servicios': servicios, 'mensaje': "Cliente encontrado"})
        else:
            return render(request, 'dashboard/dashboard.html', {'mensaje': 'Cedula no valida', 'servicios': servicios})
    return render(request, 'dashboard/dashboard.html', {'servicios': servicios})


def generar_servicio(request):
    servicios = obtener_servicios_activos()
    if request.method == 'POST':
        placa = request.POST.get('placa').upper()
        if placa is not None and validar_placa(placa):
            url = f'https://electroaires.herokuapp.com/serviciosplaca/{placa}/'
            response_placa = requests.get(url)
            data = response_placa.json()
            if data == []:
                return render(request, 'dashboard/dashboard.html', {'mensaje_placa': 'Vehiculo no encontrado', 'servicios': servicios, 'placa': placa})
            else:
                mensaje_placa = 'Vehiculo encontrado'
            return render(request, 'dashboard/dashboard.html', {'mensaje_placa': mensaje_placa, 'servicios': servicios})
        else:
            mensaje_placa = 'Placa no válida'
            return render(request, 'dashboard/dashboard.html', {'mensaje_placa': mensaje_placa, 'servicios': servicios})
    return render(request, 'dashboard/dashboard.html', {'mensaje_placa': mensaje_placa, 'servicios': servicios})


def inventario(request):
    url = 'https://electroaires.herokuapp.com/repuestos/'
    response = requests.get(url)

    if response.status_code == 200:
        dataInventario = response.json()
    else:
        dataInventario = []
        print(f"Error en la API código {response.status_code}")

    if request.method == 'POST':
        nombre_r = request.POST.get('nombre_r')
        cantidad = request.POST.get('cantidad')
        v_proveedor = request.POST.get('v_proveedor')
        v_venta = request.POST.get('v_venta')

        data = {
            'r_nombre_repuesto': nombre_r,
            'r_cantidad': cantidad,
            'r_valor_proveedor': v_proveedor,
            'r_valor_publico': v_venta
        }

        response = requests.post(url, data=data)

        if response.status_code == 201:
            if requests.get(url).status_code == 200:
                dataInventario = requests.get(url).json()
            return render(request, 'dashboard/inventario.html', {'mensaje': 'INVENTARIO ACTUALIZADO', 'dataInventario': dataInventario})
        else:
            print(f"Error en la API código LINE 135 ->{response.status_code}")

    return render(request, 'dashboard/inventario.html', {'dataInventario': dataInventario})


def ventas(request):
    return render(request, 'dashboard/ventas.html')


def buscar(request):
    if request.method == 'POST':
        placa = request.POST.get('placa').upper()
        if placa is not None and validar_placa(placa):
            print(f'{placa} -> placa válida')
            url = f'https://electroaires.herokuapp.com/serviciosplaca/{placa}/'
            response = requests.get(url)
            data = response.json()
            if data:
                return render(request, 'dashboard/buscar_vehiculo.html', {'data': data, 'mensaje': 'Vehiculo encontrado'})
            else:
                return render(request, 'dashboard/buscar_vehiculo.html', {'mensaje': 'Vehiculo NO encontrado'})
        else:
            return render(request, 'dashboard/buscar_vehiculo.html', {'mensaje': 'Placa no valida'})
    return render(request, 'dashboard/buscar_vehiculo.html')


def reportes(request):
    return render(request, 'dashboard/reportes.html')


def exit(request):
    logout(request)
    return redirect('login')
