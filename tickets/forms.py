from django import forms
from .models import Ticket, Respuesta, Tecnico
from django.contrib.auth.models import User

class TicketForm(forms.ModelForm):
    usuario = User.username

    class Meta:
        model = Ticket
        fields = ['asunto', 'descripcion', 'adjuntos']

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['tecnico', 'respuesta_texto', 'adjuntos_res', 'usuario']

class Aisgna_TecnicoForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['tecnico', 'prioridad']

class status(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['estatus']