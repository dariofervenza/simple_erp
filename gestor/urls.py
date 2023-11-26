"""
URL configuration for gestor project.

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
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import index
from .views import entrada_pedidos
from .views import entrada_facturas
from .views import lanzar_factura
from .views import datos_generales
from .views import entrada_clientes
from .views import entrada_productos
from .views import entrada_facturas
from .views import entrada_albaranes
from .views import lanzar_albaran

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("datos-generales/", datos_generales,name="datos_generales"),
    path("clientes/", entrada_clientes, name="entrada_clientes"),
    path("productos/", entrada_productos, name="entrada_productos"),
    path("pedidos/", entrada_pedidos, name="entrada_pedidos"),
    path("facturas/", entrada_facturas, name="entrada_facturas"),
    path("albaranes/", entrada_albaranes, name="entrada_albaranes"),
    path("lanzar_factura/", lanzar_factura, name="lanzar_factura"),
    path("lanzar_albaran/", lanzar_albaran, name="lanzar_albaran"),
]
