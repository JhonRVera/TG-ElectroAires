import requests
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
        username = request.POST.get('cedula')
        password = request.POST.get('contrasena')
        data = {
            'cedula': username,
            'contrasena': password
        }
        url = 'https://api-electroaires-30a0049f64a4.herokuapp.com/usuarios/verificacion/'
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
            url = 'https://api-electroaires-30a0049f64a4.herokuapp.com/clientes/'
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
        placa = request.POST.get('placa').upper()
        if validar_cedula(cedula) == True and validar_placa(placa) == True:
            cedula = request.POST.get('cedula_clt')
            placa = request.POST.get('placa').upper()
            data = {
                'cedula': cedula,
                'placa': placa,
            }
            url = 'https://api-electroaires-30a0049f64a4.herokuapp.com/verificacion-vehiculo-cliente/'
            response = requests.post(
                url, data=data, headers=autenticacion(request))
            data_clt = response.json()
            print(f'Respuesta Api {data_clt}')

            if data_clt['cedula'] == 'Cedula no existe' and data_clt['placa'] == 'Placa no existe':
                return render(request, 'dashboard/dashboard.html', {'servicios': servicios, 'mensaje': 'Crear cliente', 'cedula': cedula, 'placa': placa})

            elif data_clt['cedula'] == 'Cedula no existe':
                return render(request, 'dashboard/dashboard.html', {'servicios': servicios, 'mensaje': 'Cliente no encontrado', 'cedula': cedula})

            if data_clt['placa'] == 'Placa no existe':
                return render(request, 'dashboard/dashboard.html', {'servicios': servicios, 'mensaje': 'Vehiculo no encontrado', 'placa': placa})
            else:
                return render(request, 'dashboard/dashboard.html', {'servicios': servicios, 'mensaje': 'Generar Servicio', 'cedula': cedula, 'placa': placa})
        else:
            return render(request, 'dashboard/dashboard.html', {'servicios': servicios, 'mensaje': 'Ingrese datos validos'})
    return render(request, 'dashboard/dashboard.html', {'servicios': servicios})


def generar_servicio(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        placa = request.POST.get('placa').upper()
        if validar_cedula(cedula) == True and validar_placa(placa) == True:
            cedula = request.POST.get('cedula')
            placa = request.POST.get('placa').upper()
            descripcion = request.POST.get('descripcion')
            m_obra = request.POST.get('s_obra')
            if m_obra == '':
                m_obra = 0
            else:
                m_obra = m_obra
            data = {
                "s_descripcion": descripcion,
                "s_mano_obra": m_obra,
                "estado": True,
                "cliente": cedula,
                "s_vehiculo": placa
            }
            print(data)
            url = 'https://api-electroaires-30a0049f64a4.herokuapp.com/servicios/'
            response = requests.post(url, data=data)
            if response.status_code == 201:
                messages.success(request, 'Servicio creado correctamente')
            else:
                messages.error(request, f'Error al crear el vehiculo. Código de respuesta: {response.status_code}')
        else:
            messages.error(request, 'Ingrese datos validos')
    return redirect('dashboard')


def crear_vehiculos(request):
    if request.method == 'POST':
        placa = request.POST.get('placa').upper()
        if validar_placa(placa):
            placa = request.POST.get('placa').upper()
            tipo = request.POST.get('tipo')
            data_nuevo = {
                'placa': placa,
                'tipo': tipo,
            }
            url = 'https://api-electroaires-30a0049f64a4.herokuapp.com/vehiculos/'
            response = requests.post(
                url, data=data_nuevo, headers=autenticacion(request))
            if response.status_code == 201:
                messages.success(request, 'Vehiculo creado correctamente')
            else:
                messages.error(
                    request, f'Error al crear el vehiculo. Código de respuesta: {response.status_code}')
        else:
            messages.error(request, 'Ingrese datos validos')
    return redirect('dashboard')


def crea_clientes_vehiculos(request):
    servicios = obtener_servicios_activos()
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        placa = request.POST.get('placa').upper()
        if validar_cedula(cedula) and validar_placa(placa):
            cedula = request.POST.get('cedula')
            nombre = request.POST.get('nombre')
            celular = request.POST.get('celular')
            placa = request.POST.get('placa').upper()
            tipo = request.POST.get('tipo')

            data_cliente = {
                'cedula': cedula,
                'nombre': nombre,
                'celular': celular
            }

            data_vehiculo = {
                'placa': placa,
                'tipo': tipo,
            }
            url_vehiculos = 'https://api-electroaires-30a0049f64a4.herokuapp.com/vehiculos/'
            url_clientes = 'https://api-electroaires-30a0049f64a4.herokuapp.com/clientes/'

            response_clientes = requests.post(url_clientes, data=data_cliente, headers=autenticacion(request))
            response_vehiculos = requests.post(url_vehiculos, data=data_vehiculo, headers=autenticacion(request))

            if response_clientes.status_code == 201 and response_vehiculos.status_code == 201:
                messages.success(request, 'Vehiculo y cliente creado correctamente')
                return render(request, 'dashboard/dashboard.html', {'servicios': servicios, 'mensaje': 'Generar Servicio', 'cedula': cedula, 'placa': placa})
            else:
                messages.error(request, f'Error al crear el vehiculo. Código de respuesta: {response_clientes.status_code}')
                messages.error(request, f'Error al crear el vehiculo. Código de respuesta: {response_vehiculos.status_code}')
        else:
            messages.error(request, 'Ingrese datos validos')
    return redirect('dashboard')


def inventario(request):
    url = 'https://api-electroaires-30a0049f64a4.herokuapp.com/repuestos/'
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

def buscar(request):
    if request.method == 'POST':
        placa = request.POST.get('placa').upper()
        if placa is not None and validar_placa(placa):
            print(f'{placa} -> placa válida')
            url = f'https://api-electroaires-30a0049f64a4.herokuapp.com/serviciosplaca/{placa}/'
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
