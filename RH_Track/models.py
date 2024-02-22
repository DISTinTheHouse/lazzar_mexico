from django.db import models
from intranet.models import empleados
# Create your models here.
#Nomina
class Nomina(models.Model): #ajuste Jesus Ibarra 09/02/2024
        num_empleado = models.ForeignKey(empleados, on_delete=models.CASCADE, related_name="num_empleado")
        fecha = models.DateField()
        archivo_nomina = models.FileField(upload_to='archivos_nomina/')

        class Meta:
            verbose_name = "Nomina"
            verbose_name_plural = "Nominas"

        def __str__(self):
            return f"Nomina de {self.num_empleado} - {self.fecha}"
                
class Tabla_Nomina(models.Model): #Mayer Orozco 20/02/2024
        year = models.IntegerField(default=2024, verbose_name="Anio")
        quincena = models.IntegerField(default=0, verbose_name="Quincena")
        fecha = models.DateField()

        class Meta:
            verbose_name = "Tabla de Nomina"
            verbose_name_plural = "Tabla de Nominas"

        def __str__(self):
            return f"{self.year} - {self.quincena} - {self.fecha}"