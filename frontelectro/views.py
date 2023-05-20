from django.http import JsonResponse
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
        url = 'http://127.0.0.1:8000/usuarios/verificacion/'
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

        url = 'http://127.0.0.1:8000/clientes/verificacion/'
        response = requests.post(url, data = data)

        if response.status_code == 200:
            data_json = response.json()
            cedula = data_json['cedula']
            nombre = data_json['nombre']
            celular = data_json['celular']
            return render(request, 'dashboard/dashboard.html', {'cedula': cedula,'nombre':nombre,'celular':celular,'mensaje':'Usuario existente'})
        else:
            data = {
                'cedula': cedula,
                'nombre': nombre,
                'celular': celular

            }
            url = 'http://127.0.0.1:8000/clientes/'
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                return render(request, 'dashboard/dashboard.html', {'mensaje_sucess':'Usuario creado'})
            else:
                print(f"Error en la api codigo{ response.status_code}")
    return render(request, 'dashboard/dashboard.html')


def ventas(request):
    return render(request, 'dashboard/ventas.html')


def buscar(request):
    return render(request, 'dashboard/buscar_vehiculo.html')


def inventario(request):
    return render(request, 'dashboard/inventario.html')


def reportes(request):
    return render(request, 'dashboard/reportes.html')


def exit(request):
    logout(request)
    return redirect('login')
