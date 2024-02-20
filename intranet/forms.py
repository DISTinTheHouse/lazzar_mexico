from django import forms
from .models import *

class DiasProgramadasForm(forms.ModelForm):
    class Meta:
        model = DiasProgramadasVacaciones
        fields = ['fecha_inicio', 'fecha_final']

class BonoForm(forms.Form):
    año = forms.IntegerField(label='Año')
    mes = forms.IntegerField(label='Mes')
    quincena = forms.IntegerField(label='Quincena')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Obtener todos los empleados y agregar un campo de calificación para cada uno
        for empleado in empleados.objects.all():
            self.fields['calificacion_' + str(empleado.id)] = forms.IntegerField(label=empleado.nombre)