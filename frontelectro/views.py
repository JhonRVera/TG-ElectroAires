from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.


def home(request):
    return render(request, 'home/home.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


@login_required
def buscar(request):
    return render(request, 'dashboard/buscar_vehiculo.html')


@login_required
def inventario(request):
    return render(request, 'dashboard/inventario.html')


@login_required
def reportes(request):
    return render(request, 'dashboard/reportes.html')


@login_required
def exit(request):
    logout(request)
    return redirect('login')
