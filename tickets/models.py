from django.db import models
from django.contrib.auth.models import User

class Tecnico(models.Model):
    nombre = models.CharField(
        max_length=255,
        choices=[('Mayer', 'Mayer Orozco'), ('Jonathan', 'Jonathan Castillo'), ('Oscar', 'Oscar Zermeño'), ('Jesus', 'Jesus Ibarra')],
        default='Mayer')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    correo_tec = models.EmailField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Técnico"
        verbose_name_plural = "Técnicos"
    
    def __str__(self):
        return self.nombre

class Respuesta(models.Model):
    ticket = models.ForeignKey('Ticket', related_name='respuestas', on_delete=models.CASCADE)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    respuesta_texto = models.TextField()
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    adjuntos_res = models.FileField(upload_to='adjuntos/', null=True, blank=True)

    class Meta:
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"

class Ticket(models.Model):
    folio = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=255)
    descripcion = models.TextField()
    adjuntos = models.FileField(upload_to='adjuntos/', null=True, blank=True)
    estatus = models.CharField(
        max_length=25,
        choices=[('Abierta', 'Abierta'), ('Esperando su respuesta', 'Esperando su respuesta'), ('Resuelta', 'Resuelta')],
        default='Abierta'
    )
    fecha_alta = models.DateTimeField(auto_now_add=True)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, null=True, blank=True)
    prioridad = models.CharField(max_length=20, null=True, blank=True)
    respuestas_Tec = models.ManyToManyField(Respuesta, related_name='respuestas_ticket')

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def agregar_respuesta(self, tecnico, respuesta_texto, adjuntos_res, usuario):
        respuesta = Respuesta(ticket=self, tecnico=tecnico, respuesta_texto=respuesta_texto, adjuntos_res=adjuntos_res, usuario=usuario)
        respuesta.save()
        #self.respuestas.add(respuesta)
        self.save()

    def asignar_tecnico(self, tecnico_id, prioridad):
        self.tecnico = tecnico_id,
        self.prioridad = prioridad
        self.save()
    
    def cambia_estatus(self, estatus):
        self.estatus = estatus
        self.save()