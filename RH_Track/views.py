from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from openpyxl import load_workbook
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from .models import Nomina, Tabla_Nomina
from intranet.models import empleados
from mainapp.models import CorreosLazzar
import os

@login_required(login_url="login")
def horarios(request):
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 03/01/2024
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups

    if request.method == 'POST':

        hora_inicio_str = request.POST.get('hora_inicio')
        hora_fin_str = request.POST.get('hora_fin')


        hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
        hora_fin = datetime.strptime(hora_fin_str, '%H:%M').time()

        diferencia_tiempo = resta_de_horas(hora_fin, hora_inicio)

        diferencia_formateada = str(diferencia_tiempo)
        
        color = 'green' if diferencia_tiempo >= timedelta(hours=9, minutes=30) else 'red'

        return render(request, 'horarios.html', {
            'diferencia_tiempo': diferencia_formateada,
            'color':color,
            'ventas': ventas, #Admin-Groups Jesus Ibarra 03/01/2024
            'acceso_total': acceso_total,
            'mesa_control': mesa_control, # End Admin-Groups
            })

    return render(request, 'horarios.html',{
        'ventas': ventas, #Admin-Groups Jesus Ibarra 03/01/2024
        'acceso_total': acceso_total,
        'mesa_control': mesa_control, # End Admin-Groups
    })

def resta_de_horas(hora_fin, hora_inicio):

    fecha_actual = datetime.now().date()
    dt_inicio = datetime.combine(fecha_actual, hora_inicio)
    dt_fin = datetime.combine(fecha_actual, hora_fin)

    diferencia_tiempo = dt_fin - dt_inicio

    return diferencia_tiempo

def vacaciones(request):
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 03/01/2024
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups

   # puestos_usuarios = ["sistemas", "ventas", "bordados", "RH",]

    #if "sistemas" in puestos_usuarios and request.user.groups.filter(name='Mayer').exists():
   #     usuarios = CorreosLazzar.objects.filter(puesto="sistemas")
  #  elif "ventas" in puestos_usuarios and request.user.groups.filter(name='Alexander').exists():
 #       usuarios = CorreosLazzar.objects.filter(puesto="ventas")
#    elif "bordados" in puestos_usuarios and request.user.groups.filter(name='Mauricio').exists():
    #    usuarios = CorreosLazzar.objects.filter(puesto="bordados") 
   # elif "RH" in puestos_usuarios and request.user.groups.filter(name='Jimena').exists():
  #      usuarios = CorreosLazzar.objects.filter(puesto="RH")
 #   else:
       # usuarios = CorreosLazzar.objects.none()  

    #usuarios = CorreosLazzar.objects.filter(puesto__in=puestos_usuarios) -----CASOS PARA VERIFICAR TODA LA TABLA

    return render(request, 'vacaciones.html', {
  #      'usuarios': usuarios,
        'ventas': ventas,
        'acceso_total': acceso_total,
        'mesa_control': mesa_control,

    })

@login_required(login_url="login")
def ver_nomina(request): #Ajuste Jes  s Ibarra 09/02/2024
    try:
        # obtener el usuario registrado en CorreosLazzar
        usuario_correos_lazzar = CorreosLazzar.objects.get(correo=request.user.email)

        # Si es CorreosLazzar, mostrar solo las n  minas asociadas a ese usuario
        nominas = Nomina.objects.filter(num_empleado__codigo=usuario_correos_lazzar.num_empleado)
        context = {
            'nominas': nominas,
            'usuario_correos_lazzar': usuario_correos_lazzar,
            'usuario_empleado': None,
        }

    except CorreosLazzar.DoesNotExist:
        try:
            # obtener el empleado asociado al usuario actual
            usuario_empleado = empleados.objects.get(codigo=request.user.username)

            # Si es Empleados, mostrar solo las n  minas para el empleado actual
            nominas = Nomina.objects.filter(num_empleado=usuario_empleado)
            context = {
                'nominas': nominas,
                'usuario_correos_lazzar': None,
                'usuario_empleado': usuario_empleado,
            }

        except empleados.DoesNotExist: #si no existe entonces:
            return redirect('login')

    return render(request, 'nomina.html', context)

@login_required(login_url="login")
def ver_nomina_propuesta(request): #MAYER OROZCO 20/02/2024
    try:
        # obtener el usuario registrado en CorreosLazzar
        usuario_correos_lazzar = CorreosLazzar.objects.get(correo=request.user.email)
        usuario_empleado = empleados.objects.get(codigo=usuario_correos_lazzar.num_empleado)

        # Si es CorreosLazzar, mostrar solo las nominas asociadas a ese usuario
        periodos = Tabla_Nomina.objects.all().values_list('year', 'quincena', 'fecha')
        codigo_empleado = '0'
        nomias = []

        for year, quincena, fecha in periodos:
            ruta_pdf = os.path.join('mainapp', 'static', 'nominas', str(year), str(quincena))
            
            if len(str(usuario_correos_lazzar.num_empleado)) == 1:
                codigo_empleado = "00" + str(usuario_correos_lazzar.num_empleado)
            elif len(str(usuario_correos_lazzar.num_empleado)) == 2:
                codigo_empleado = "0" + str(usuario_correos_lazzar.num_empleado)
            else:
                codigo_empleado = str(usuario_correos_lazzar.num_empleado)

            prefijo = "RE_3105_Quincenal_" + str(year) +"_" + str(quincena) + "_" + codigo_empleado

            archivos = os.listdir(ruta_pdf)

            for archivo in archivos:
                if archivo.startswith(prefijo):
                    ruta_completa = os.path.join('nominas', str(year), str(quincena), archivo)
                    nomias.append([ruta_completa, fecha])

        context = {
            'nominas': nomias,
            'nombre': usuario_empleado.nombre,
            'apellido_paterno': usuario_empleado.apellido_paterno,
        }

    except CorreosLazzar.DoesNotExist:
        try:
            # obtener el empleado asociado al usuario actual
            usuario_empleado = empleados.objects.get(codigo=request.user.username)

            # Si es CorreosLazzar, mostrar solo las nominas asociadas a ese usuario
            periodos = Tabla_Nomina.objects.all().values_list('year', 'quincena', 'fecha')
            codigo_empleado = '0'
            nomias = []

            for year, quincena, fecha in periodos:
                ruta_pdf = os.path.join('mainapp', 'static', 'nominas', str(year), str(quincena))
                
                if len(str(usuario_empleado.codigo)) == 1:
                    codigo_empleado = "00" + str(usuario_empleado.codigo)
                elif len(str(usuario_empleado.codigo)) == 2:
                    codigo_empleado = "0" + str(usuario_empleado.codigo)
                else:
                    codigo_empleado = str(usuario_empleado.codigo)

                prefijo = "RE_3105_Quincenal_" + str(year) +"_" + str(quincena) + "_" + codigo_empleado

                archivos = os.listdir(ruta_pdf)

                for archivo in archivos:
                    if archivo.startswith(prefijo):
                        ruta_completa = os.path.join('nominas', str(year), str(quincena), archivo)
                        nomias.append([ruta_completa, fecha])

            context = {
                'nominas': nomias,
                'nombre': usuario_empleado.nombre,
                'apellido_paterno': usuario_empleado.apellido_paterno,
            }
        except empleados.DoesNotExist: #si no existe entonces:
            return redirect('login')

    return render(request, 'nomina.html', context)
