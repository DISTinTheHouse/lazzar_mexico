from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('intranet/', views.index_intranet, name='inicio_intranet'),
    path('inicio_portal/', views.inicio_portal, name='inicio_portal'),
    path('directorio/', views.directorio, name='directorio'),
    path('organizacion/', views.organizacion, name='organizacion'),
    path('mision_vision/', views.mision_vision, name='mision_y_vision'),
    path('valores/', views.valores, name='valores'),
    path('codigo_etica/', views.codigoe, name='codigoe'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contribucion/', views.contribucion, name='contribucion'),
    path('recursoshumanos/', views.recursoshumanos, name='recursoshumanos'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('catalogo_empleados/', views.catalogo_empleados, name='catalogo_empleados'),
    path('actualiza_bono/', views.actualiza_bono, name='actualiza_bono'),
    path('confirmacion_actualizacion/', views.confirmacion_actualizacion, name='confirmacion_actualizacion'),
    path('vacation_days/', views.vacation_days, name='vacation_days'),
    path('programar_dias/<int:empleado_id>/', views.programar_dias, name='programar_dias'),
    path('eliminar_programacion/<int:prog_id>/', views.eliminar_programacion, name='eliminar_programacion'),
    path('descarga_pdf/<int:prog_id>/', views.descarga_pdf, name='descarga_pdf'),
    path('reglamentointerno/', views.reglamento, name='reglamentoi'),
    path('organigrama/', views.reglamento, name='organigrama'),
    path('macroproceso/', views.macroproceso, name='macroproceso'),
    path('descripcionesdepuesto/', views.descripcionesdepuesto, name='descripcionesdepuesto'),
    path('bono/', views.mostrar_bono, name='bono'),
    path('avisoprivacidad/', views.avisop, name='avisop'),
]