from django.db import models

# Create your models here.
class CorreosLazzar(models.Model):
    id = models.IntegerField(primary_key= True)
    correo = models.EmailField(max_length=200, verbose_name="Correo")
    esvendedor = models.BooleanField(verbose_name="Es Vendedor?")
    cod_Proscai = models.CharField(default="", max_length= 4, verbose_name="Codigo Proscai")
    nombre = models.CharField(default="", max_length= 250, verbose_name="Nombre")
    group_Proscai = models.CharField(default="", max_length= 250, verbose_name="Grupo Proscai")
    num_empleado = models.IntegerField(default=0, verbose_name="Código Empleado")
    admin_group = models.BooleanField(default=False,verbose_name="Admin Grupo?")
    vender_group = models.BooleanField(default=False, verbose_name="Vendedor Solo?")
    administrador = models.BooleanField(default=False, verbose_name="Es Administrador?")

    class Meta:
        verbose_name = "Correo"
        verbose_name_plural = "Correos"

    def __str__(self):
        return self.correo