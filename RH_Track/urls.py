from django.urls import path
from . import views

urlpatterns = [
    path('horarios/',views.horarios, name="horarios"),
    path('vacaciones/',views.vacaciones, name="vacaciones"),
    path('nomina/',views.ver_nomina, name='nomina'),
    path('ver_nomina_propuesta/',views.ver_nomina_propuesta, name='ver_nomina_propuesta'),
]
