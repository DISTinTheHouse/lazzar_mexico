from django.db import models

# Create your models here.
class codigo_almacen(models.Model):
    id_almacen = models.IntegerField(primary_key= True)
    cod_almacen = models.CharField(default="", max_length= 3, verbose_name="Codigo Almacen")
    nombre_almacen = models.CharField(default="", max_length= 250, verbose_name="Nombre Almacen")

    class Meta:
        verbose_name = "Codigo Almacen"
        verbose_name_plural = "Codigo Almacens"

    def __str__(self):
        return self.cod_almacen

