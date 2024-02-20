from django.urls import path
from . import views

urlpatterns = [ 
    path('pedidos_index/', views.pedidos_index, name="pedidos_index"),
    path('materiales/', views.materiales, name="materiales"),
    path('telas_stock/', views.telas, name="telas_stock"),
    path('stock_alm/', views.stock_alm, name="stock_alm"),
    path('descargar_excel_04/', views.descargar_excel_04, name="descargar_excel_04"),
    path('descargar_excel_avios/', views.descargar_excel_avios, name="descargar_excel_avios"),
    path('pedidos_q/', views.pedidos_q, name="pedidos_q"),
    path('ordenes_e/', views.ordenes_e, name="ordenes_e"),
    path('detalle_ordenes_e/', views.detalle_ordenes_e, name="detalle_ordenes_e"),
    path('pedidos_pq/', views.pedidos_pq, name="pedidos_pq"),
    path('search_pq/', views.search_pq, name="search_pq"),
    path('search_q/', views.search_q, name="search_q"),
    path('search_e/', views.search_e, name="search_e"),
    path('orden_e_vencido/', views.orden_e_vencido, name="orden_e_vencido"),
]