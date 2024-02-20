from django.urls import path
from . import views

urlpatterns = [
    # path('<str:slug>/', views.page, name="page")
    path('nosotros/',views.nosotros, name="nosotros"),
    path('enviar_correo/', views.enviar_correo, name='enviar_correo'),

]
