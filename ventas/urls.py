from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('facturacion/',views.facturas, name="facturacion"),
    path('facturas_fecha/',views.facturas_fecha, name="facturas_fecha"),
    path('chats/',views.chats, name="chats"),
    path('chats_fecha/',views.chats_fecha, name="chats_fecha"),
    path('correos/',views.correos, name="correos"),
    path('correos_fecha/',views.correos_fecha, name="correos_fecha"),
    path('comercial/',views.comercial, name="comercial"),
    path('status/',views.status, name="status"),
    path('status_pedido/',views.status_pedido, name="status_pedido"),
    path('status_pedido_index', views.status_pedido_index, name="status_pedido_index"),
    path('cartera/',views.cartera, name="cartera"),
    path('pedido_cliente/',views.pedido_cliente, name="pedido_cliente"),
    path('existencias/', views.existencias, name="existencias"),
    path('embarque/',views.embarque, name="embarque"),
    path('embarque_vender/', views.embarque_vender, name="embarque_vender"),
    path('detalle_activos_ventas/', views.detalle_activos_ventas, name="detalle_activos_ventas"),
    path('ingresados/',views.ingresados, name="ingresados"),
    path('ingresados_vender/', views.ingresados_vender, name="ingresados_vender"),
    path('embarque_pedido/', views.embarque_pedido, name="embarque_pedido"),
    path('embarque_muestras/', views.embarque_muestras, name="embarque_muestras"),
    path('embarque_muestras_vendedor/', views.embarque_muestras_vendedor, name="embarque_muestras_vendedor"),
]