from django.urls import path
from . import views

urlpatterns = [
    path('pedidos/',views.pedidos, name="pedidos"),
    path('entregados_folios/',views.entregados_folios, name="entregados_folios"),
    path('entregados_fecha/',views.entregados_fecha, name="entregados_fecha"),
    path('pendientes_folios/',views.pendientes_folios, name="pendientes_folios"),
    path('dashboard_Bord/',views.dashboard_Bord, name="dashboard_Bord"),
    path('descargar_excel/', views.descargar_excel, name='descargar_excel'),
    path('buscar_ventas/',views.buscar_ventas, name="buscar_ventas"),
    path('detalle_bordados/',views.detalle_bordados, name="detalle_bordados"),
    path('pedidos_dia/', views.pedidos_dia, name="pedidos_dia"),
    path('historial/', views.productividad, name='historial'),
    path('descargar_excel_productividad/', views.descargar_excel_productividad, name='descargar_excel_productividad'),
]