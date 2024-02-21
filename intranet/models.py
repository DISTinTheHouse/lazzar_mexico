from django.db import models
import datetime


# Tipo de Contratos
class tipo_contratos(models.Model):
    id = models.AutoField(primary_key= True, verbose_name="id")
    contrato = models.CharField(max_length=250, verbose_name="Tipo de contrato")

    class Meta:
        verbose_name = "Tipo de Contrato"
        verbose_name_plural = "Tipo de Contrato"

    def __str__(self):
        return self.contrato
    
# Departamento
class departamento(models.Model):
    id = models.AutoField(primary_key= True, verbose_name="id")
    Departamento = models.CharField(max_length=250, verbose_name="Departamento")

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamento"

    def __str__(self):
        return self.Departamento
    
# Puesto
class puesto(models.Model):
    id = models.AutoField(primary_key= True, verbose_name="id")
    Puesto = models.CharField(max_length=250, verbose_name="Puesto")
    departamento = models.ForeignKey(departamento, on_delete=models.CASCADE, related_name='puestos')

    class Meta:
        verbose_name = "Puesto"
        verbose_name_plural = "Puestos"

    def __str__(self):
        return f"{self.Puesto} - {self.departamento}"
    
# Ubicación
class ubicacion(models.Model):
    id = models.AutoField(primary_key= True, verbose_name="id")
    ubicacion = models.CharField(max_length=250, verbose_name="Ubicación")

    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciónes"

    def __str__(self):
        return self.ubicacion

# Empleados
class empleados(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    codigo = models.IntegerField(unique=True, verbose_name="Código")
    fecha_alta = models.DateField(verbose_name="Fecha Alta")
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name="Fecha Vencimiento")
    apellido_paterno = models.CharField(max_length=250, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=250, verbose_name="Apellido Materno")
    nombre = models.CharField(max_length=250, verbose_name="Nombre")
    correo_instucional = models.EmailField(null=True, blank=True, max_length=250, verbose_name="Correo Lazzar")
    correo_nomina = models.EmailField(null=True, blank=True, max_length=250, verbose_name="Correo")
    codigo_jefe = models.IntegerField(default=0, verbose_name="Código Jefe Inmediato")
    jefe = models.CharField(max_length=250, verbose_name="Jefe Inmediato")
    baja = models.BooleanField(default=False, verbose_name="¿Es Baja?")
    fecha_baja = models.DateField(null=True, blank=True, verbose_name="Fecha Baja")
    fecha_modificacion = models.DateField(auto_now=True, verbose_name="Ultima Modificación")
    contrato = models.ForeignKey(tipo_contratos, on_delete=models.CASCADE, related_name='tipo_de_contrato')
    puesto = models.ForeignKey(puesto, on_delete=models.CASCADE, related_name='puesto')
    departamento = models.ForeignKey(departamento, on_delete=models.CASCADE, related_name='departamento')
    ubicacion = models.ForeignKey(ubicacion, on_delete=models.CASCADE, related_name='centro_de_trabajo_empleados')
    fecha_cumpleaños = models.DateField(null=True, blank=True, verbose_name="Fecha Cumpleaños")
    correo_cumple_enviado = models.BooleanField(default=False)
    correo_aniversario_enviado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        return f"{self.codigo} - {self.nombre} {self.apellido_paterno} {self.apellido_materno} - {self.codigo_jefe} - {self.baja}"
    
class Imagen(models.Model):
    imagen = models.ImageField(upload_to='static/img/noticias')

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imagenes"

class dias_disponibles_vacaciones(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    saldo_anterior = models.IntegerField(default=0, verbose_name="Saldo año anterior")
    dias_vacaciones = models.IntegerField(default=0, verbose_name="Días de vacaciones")
    semana_santa = models.IntegerField(default=6, verbose_name="Semana Santa")
    saldo_actual = models.IntegerField(default=0, verbose_name="Saldo actual")
    programados = models.IntegerField(default=0, verbose_name="Días programados")
    dias_tomados = models.IntegerField(default=0, verbose_name="Días tomados")
    saldo_final = models.IntegerField(default=0, verbose_name="Saldo final")
    dato_empleado = models.ForeignKey(empleados, on_delete=models.CASCADE, related_name='dato_empleado')

    def __str__(self):
        return f"{self.dato_empleado.codigo} - {self.dato_empleado.apellido_paterno} - {self.dato_empleado.apellido_materno} - {self.dato_empleado.nombre} - {self.saldo_final}"
    
class DiasProgramadasVacaciones(models.Model):
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_final = models.DateField(verbose_name="Fecha de Finalización")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Modificación")
    prog_empleado = models.ForeignKey(empleados, on_delete=models.CASCADE, related_name='prog_empleado')

    def __str__(self):
        return f"Vacaciones de {self.prog_empleado.codigo} - {self.prog_empleado.apellido_paterno} - {self.prog_empleado.apellido_materno} - {self.prog_empleado.nombre} - del {self.fecha_inicio} al {self.fecha_final}"

class bono(models.Model):
    id = models.AutoField(primary_key= True, verbose_name="id")
    Año = models.IntegerField(default=2024, verbose_name="Año")
    Mes = models.IntegerField(default=0, verbose_name="Mes" )
    Quincena = models.IntegerField(default=0, verbose_name="Quincena" )
    Calificacion = models.IntegerField(default=0, verbose_name="Calificación")
    cal_empleado = models.OneToOneField(empleados, on_delete=models.CASCADE, related_name='cal_empleado', verbose_name="Empleado")

    class Meta:
        verbose_name = "Bono"

    def __str__(self):
        return f"{self.Año} - {self.Mes} - {self.Quincena} - {self.Calificacion} - {self.cal_empleado.codigo}"
    

    
    


    