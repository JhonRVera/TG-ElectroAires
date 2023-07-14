"""
URL configuration for electroaires project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import home, login, dashboard, buscar, inventario, reportes, exit, crear_vehiculos, crear_cliente,generar_servicio,crea_clientes_vehiculos
from .ventas_views import ventas,repuestos
urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('crear_cliente/', crear_cliente, name='crear_cliente'),
    path('crear_vehiculos/', crear_vehiculos, name='crear_vehiculos'),
    path('generar_servicio/', generar_servicio, name='generar_servicio'),
    path('crea_clientes_vehiculos/', crea_clientes_vehiculos, name='crea_clientes_vehiculos'),
    path('buscar/', buscar, name='buscar'),
    path('ventas/', ventas, name='ventas'),
    path('repuestos/', repuestos, name='repuestos'),
    path('inventario/', inventario, name='inventario'),
    path('reportes/', reportes, name='reportes'),
    path('logout/', exit, name='exit'),
]
