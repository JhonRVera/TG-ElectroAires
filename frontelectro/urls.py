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
from .views import home, login, dashboard, buscar, inventario, reportes, exit, ventas, eliminar_producto

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('buscar/', buscar, name='buscar'),
    path('ventas/', ventas, name='ventas'),
    path('inventario/', inventario, name='inventario'),
    path('reportes/', reportes, name='reportes'),
    path('logout/', exit, name='exit'),
    path('eliminar_producto/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),

]
