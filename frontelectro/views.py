import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from frontelectro.utils.funciones_especiales import validar_placa
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


def dashboard(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        nombre = request.POST.get('nombre')
        celular = request.POST.get('celular')

        # Verificar cliente existente
        data = {
            'cedula': cedula
        }
        url = 'https://electroaires.herokuapp.com/clientes/verificacion/'
        response = requests.post(
            url, data=data, headers=autenticacion(request))
        print(f"DATOS DE CLIENTE EXISTENTE {response.json()}")
        if response.status_code == 200:
            data_json = response.json()
            cedula = data_json['cedula']
            nombre = data_json['nombre']
            celular = data_json['celular']
            return render(request, 'dashboard/dashboard.html', {'cedula': cedula, 'nombre': nombre, 'celular': celular, 'mensaje': 'Usuario existente'})

        # Crear nuevo cliente
        data = {
            'cedula': cedula,
            'nombre': nombre,
            'celular': celular
        }
        url = 'https://electroaires.herokuapp.com/clientes/'
        response = requests.post(
            url, data=data, headers=autenticacion(request))
        print(f"DATOS DE CLIENTE NUEVO {response.json()}")
        if response.status_code == 200:
            return render(request, 'dashboard/dashboard.html', {'mensaje_sucess': 'Usuario creado'})
        else:
            print(
                f"Error en la API al agregar cliente (código: {response.status_code})")

    # Obtener servicios activos
    url = 'https://electroaires.herokuapp.com/servicios/'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        servicios = []
        for item in data:
            servicio_id = item['id']
            vehiculo = item['s_vehiculo']
            estado = item['estado']
            if estado == True:
                estado = 'ACTIVO'
            else:
                estado = 'INACTIVO'
            servicios.append(
                {'id': servicio_id, 'vehiculo': vehiculo, 'estado': estado})

        return render(request, 'dashboard/dashboard.html', {'servicios': servicios})
    else:
        print('Error al obtener los servicios activos')
        return render(request, 'dashboard/dashboard.html', {'servicios': []})


def generar_servicio(request):
    mensaje = None
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        placa = request.POST.get('placa')
        if validar_placa(placa) == True:
            mensaje = 'Usuario placa válida'
        else:
            mensaje = 'Usuario placa no válida'
    return render(request, 'dashboard/dashboard.html', {'mensaje': mensaje})


def eliminar_producto(request, producto_id):
    url = f'https://electroaires.herokuapp.com/repuestos/{producto_id}/'
    response = requests.delete(url)

    if response.status_code == 204:
        return redirect('inventario')
    else:
        print(f"Error en la API código LINE 100 -> {response.status_code}")

    return redirect('inventario')


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
            url = f'https://electroaires.herokuapp.com/vehiculos/{placa}/'
            response = requests.get(url)
            data = response.json()
            print(data)
            return render(request, 'dashboard/buscar_vehiculo.html', {'data': data,'mensaje':'Vehiculo encontrado'})
        else:
            print(f'{placa} -> no válida')
            return render(request, 'dashboard/buscar_vehiculo.html', {'mensaje':'Placa no valida'})
    return render(request, 'dashboard/buscar_vehiculo.html')


def reportes(request):
    return render(request, 'dashboard/reportes.html')


def exit(request):
    logout(request)
    return redirect('login')
