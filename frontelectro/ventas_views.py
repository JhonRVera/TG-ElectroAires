import requests
from django.contrib import messages
from django.shortcuts import redirect, render
from frontelectro.utils.funciones_especiales import validar_cedula
from frontelectro.utils.autenticacion import autenticacion


def ventas(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        if cliente == '':
            return render(request, 'dashboard/ventas.html', {'mensaje': 'Los campos no deben estar vacios'})
        if validar_cedula(cliente):
            cliente = request.POST.get('cliente')
            url = f'https://api-electroaires-30a0049f64a4.herokuapp.com/clientes/{cliente}'
            response = requests.get(url, headers=autenticacion(request))
            if response.status_code == 200:
                cliente = response.json()
                cedula = cliente['cedula']
                nombre = cliente['nombre']
                celular = cliente['celular']
                return render(request, 'dashboard/ventas.html', {'nombre': nombre, 'celular': celular, 'cedula': cedula})
            else:
                print(f"Error en la API código {response.status_code}")
                return render(request, 'dashboard/ventas.html', {'mensaje': 'Cliente no encontrado'})
        else:
            return render(request, 'dashboard/ventas.html', {'mensaje': 'Ingrese una placa valida'})
    else:
        return render(request, 'dashboard/ventas.html')


def repuestos(request):
    if request.method == 'POST':
        id_repuesto = request.POST.get('codigo')
        cantidad = request.POST.get('codigo')
        data = zip(id_repuesto,cantidad)
        if data == '' :
            messages.error(request, 'Los campos no pueden estar vacios')
            return redirect('ventas')
        url = f'https://api-electroaires-30a0049f64a4.herokuapp.com/repuestos/{id_repuesto}'
        response = requests.get(url, headers=autenticacion(request))
        if response.status_code == 200:
            repuestos = response.json()
            return render(request, 'dashboard/ventas.html', {'repuestos': repuestos})
        else:
            print(f"Error en la API código {response.status_code}")
            messages.error(request, 'Codigo no encontrado')
            return redirect('ventas')
        
    else:
        return render(request, 'dashboard/ventas.html')
