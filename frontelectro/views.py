import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login

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

        data = {
            'cedula': cedula
        }

        url = 'https://electroaires.herokuapp.com/clientes/verificacion/'
        response = requests.post(url, data=data)

        if response.status_code == 200:
            data_json = response.json()
            cedula = data_json['cedula']
            nombre = data_json['nombre']
            celular = data_json['celular']
            return render(request, 'dashboard/dashboard.html', {'cedula': cedula, 'nombre': nombre, 'celular': celular, 'mensaje': 'Usuario existente'})
        else:
            data = {
                'cedula': cedula,
                'nombre': nombre,
                'celular': celular

            }
            url = 'https://electroaires.herokuapp.com/clientes/'
            response = requests.post(url, data=data)

            if response.status_code == 200:
                return render(request, 'dashboard/dashboard.html', {'mensaje_sucess': 'Usuario creado'})
            else:
                print(f"Error en la api codigo{ response.status_code}")
    return render(request, 'dashboard/dashboard.html')

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
            print(f"Error en la API código {response.status_code}")

    return render(request, 'dashboard/inventario.html', {'dataInventario': dataInventario})

def ventas(request):
    return render(request, 'dashboard/ventas.html')


def buscar(request):
    return render(request, 'dashboard/buscar_vehiculo.html')


def reportes(request):
    return render(request, 'dashboard/reportes.html')


def exit(request):
    logout(request)
    return redirect('login')
