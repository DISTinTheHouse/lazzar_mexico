from django.urls import path
from . import views

urlpatterns = [
    path('pedidos_produccion/', views.pedidos_produccion, name="pedidos_produccion"),
    path('stock/', views.stock, name="stock"),
    path('pedidos_ep/', views.pedidos_ep, name="pedidos_ep"),
    path('produccion_activos/', views.produccion_activos, name="produccion_activos"),
    path('pedidos_cedicor/', views.pedidos_cedicor, name="pedidos_cedicor"),

]