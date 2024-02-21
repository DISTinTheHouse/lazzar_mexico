from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from mainapp.models import CorreosLazzar
from intranet.models import *
from django.contrib import messages
from .forms import *
import datetime
import math
import numpy as np
from django.utils import timezone
from django.template.loader import render_to_string
from datetime import datetime
import pdfkit
from django.core.mail import send_mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from django.urls import reverse


def index_intranet(request):
    imagenes = Imagen.objects.all()
    num_imagenes = len(imagenes)
    
    mes_actual = datetime.now().month

    usuarios = empleados.objects.filter(fecha_cumpleaños__month=mes_actual).order_by('fecha_cumpleaños__day')
    usuariosa = empleados.objects.filter(fecha_alta__month=mes_actual).order_by('fecha_alta__day') #oscar zermeño 16/02/2024
    
    for usuario in usuarios:
        if usuario.fecha_cumpleaños.day == datetime.now().day:  # Es el cumpleaños hoy
            cumpleañero = empleados.objects.get(codigo=usuario.codigo)
            if request.method == "POST" and cumpleañero.correo_cumple_enviado == False: #Ajuste Jesús Ibarra 09/02/2024 ---
                enviar_correo_feliz_cumple(usuario)
                cumpleañero.correo_cumple_enviado = True
                cumpleañero.save() #----------------------------------------------------------------

    for usuario in usuariosa:
        if usuario.fecha_alta.day == datetime.now().day:  # Es el aniversario hoy
            empleado = empleados.objects.get(codigo=usuario.codigo)
            if request.method == "POST" and not empleado.correo_aniversario_enviado:
                enviar_correo_aniversario(usuario)
                empleado.correo_aniversario_enviado = True
                empleado.save()
            

    context = {
        'imagenes': imagenes,
        'num_imagenes': num_imagenes,
        'usuarios': usuarios,
        'usuariosa': usuariosa, #oscar zermeño 16/02/2024
    }
    return render(request, 'index_intranet.html', context)

def enviar_correo_feliz_cumple(usuario):


    # MAYER OROZCO 15/02/2024
    nombre = usuario.nombre
    ruta_imagen_cumple = os.path.join('mainapp', 'static', 'correos', 'cumpleaños.png')

    # Adjuntar las imágenes al mensaje MIME
    with open(ruta_imagen_cumple, 'rb') as f:
        imagen1 = MIMEImage(f.read())
        imagen1.add_header('Content-ID', '<imagen1>')  # Identificador para la imagen1

    # Configuración del mensaje
    msg = MIMEMultipart()
    msg['From'] = 'sistemas@lazzarmexico.com'
    msg['To'] = usuario.correo_nomina
    msg['Subject'] = '¡Feliz Cumpleaños ' + nombre + '!'

    # Cuerpo del mensaje en HTML
    html = f"""
        <html lang="es">
        <head>
            <style>
                body {{
                    background-color: #ADD8E6;
                    text-align: center;
                }}
                p {{
                    margin: 0 auto; /* Centrar párrafos */
                    padding: 10px; /* Espaciado interior */
                }}
            </style>
        </head>
        <body style>
            <h1>¡Querido {nombre}!</h1>
            <p>En este día especial, en Lazzar nos tomamos un momento para enviarte nuestras más sinceras felicitaciones. ¡Felicidades!</p>
            <p>Que este día esté lleno de alegría, amor y momentos inolvidables. Que cada momento que vivas te traiga más felicidad y satisfacción.</p>
            <p>Recuerda siempre que mereces lo mejor en la vida y estamos seguros de que seguirás alcanzando grandes logros y cosechando éxitos.</p>
            <p>Celebra este día en compañía de tus seres queridos y nunca olvides lo especial que eres para todos nosotros.</p>
            <img src="cid:imagen1">
        </body>
        </html>
    """
    destinatarios = obtener_destinatarios('destinatarios.txt')
    total_destinatarios = destinatarios + [usuario.correo_nomina]

    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(html, 'html'))

    # Adjuntar las imágenes al mensaje MIME
    with open(ruta_imagen_cumple, 'rb') as f:
        imagen1 = MIMEImage(f.read())
        imagen1.add_header('Content-ID', '<imagen1>')  # Identificador para la imagen1
        msg.attach(imagen1)

    # Enviar el correo
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('sistemas@lazzarmexico.com', 'nldflybxyeiukvko')
        server.sendmail('sistemas@lazzarmexico.com', total_destinatarios, msg.as_string())
        server.quit()
        print("Correo enviado correctamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def enviar_correo_aniversario(usuario):


    # MAYER OROZCO 15/02/2024     #oscar zermeño 16/02/2024
    nombre = usuario.nombre
    ruta_imagen_cumple = os.path.join('mainapp', 'static', 'correos', 'aniversario.png')

    # Adjuntar las imágenes al mensaje MIME
    with open(ruta_imagen_cumple, 'rb') as f:
        imagen1 = MIMEImage(f.read())
        imagen1.add_header('Content-ID', '<imagen1>')  # Identificador para la imagen1

    # Configuración del mensaje
    msg = MIMEMultipart()
    msg['From'] = 'sistemas@lazzarmexico.com'
    msg['To'] = usuario.correo_nomina
    msg['Subject'] = '¡Feliz Aniversario ' + nombre + '!'

    # Cuerpo del mensaje en HTML
    html = f"""
        <html lang="es">
        <head>
            <style>
                body {{
                    background-color: #ADD8E6;
                    text-align: center;
                }}
                p {{
                    margin: 0 auto; /* Centrar párrafos */
                    padding: 10px; /* Espaciado interior */
                }}
            </style>
        </head>
        <body style>
            <h1>¡Querido {nombre}!</h1>
            <p>Recuerda que eres más que solo un número, o un día en el calendario, 
            eres un elemento muy importante para Lazzar, agradecemos tu permanencia, 
            dedicación y valiosa contribución</p>
            <img src="cid:imagen1">
        </body>
        </html>
    """
    destinatarios = obtener_destinatarios('destinatarios.txt')
    total_destinatarios = destinatarios + [usuario.correo_nomina]

    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(html, 'html'))

    # Adjuntar las imágenes al mensaje MIME
    with open(ruta_imagen_cumple, 'rb') as f:
        imagen1 = MIMEImage(f.read())
        imagen1.add_header('Content-ID', '<imagen1>')  # Identificador para la imagen1
        msg.attach(imagen1)

    # Enviar el correo
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('sistemas@lazzarmexico.com', 'nldflybxyeiukvko')
        server.sendmail('sistemas@lazzarmexico.com', total_destinatarios, msg.as_string())
        server.quit()
        print("Correo enviado correctamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")        

def obtener_destinatarios(nombre_archivo):
    ruta_archivo = os.path.join('mainapp', 'static', 'correos', nombre_archivo)

    try:
        with open(ruta_archivo, 'r') as f:
            destinatarios = [line.strip() for line in f if line.strip()]
        return destinatarios
    except FileNotFoundError:
        print(f"El archivo '{ruta_archivo}' no se encontró.")
        return []


def directorio(request):
    return render(request, 'directorio.html')

def organizacion(request):
    return render(request, 'organizacion.html')

def mision_vision(request):
    return render(request, 'mision_y_vision.html')

def valores(request):
    return render(request, 'valores.html')

def codigoe(request):
    return render(request, 'codigo de etica.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def contribucion(request):
    return render(request, 'contribucion lazzar.html')

def recursoshumanos(request):
    return render(request, 'recursos humanos.html')

def cedicor(request):
    return render(request, 'cedicor.html')

@login_required(login_url="login")
def catalogo_empleados(request):
    lista_empleados = empleados.objects.all()

    return render(request, 'catalogo_empleados.html', {
        'empleados': lista_empleados,
        })

@login_required(login_url="login")
def actualiza_bono(request):
    # Procesar el formulario para el año y el mes
    if request.method == 'POST':
        año = request.POST.get('año')
        mes = request.POST.get('mes')
        quincena = request.POST.get('quincena')

        # Procesar el formulario para las calificaciones de los empleados
        for empleado in empleados.objects.all():
            calificacion = request.POST.get('calificacion_' + str(empleado.id))

            # Verificar si ya existe un bono para este empleado en el año y mes especificados
            bono_existente = bono.objects.filter(Año=año, Mes=mes, Quincena=quincena, cal_empleado=empleado)
            if bono_existente.exists():
                bono_existente.update(Calificacion=calificacion)
            else:
                # Si no existe un bono para este empleado en el año y mes especificados, crear uno nuevo
                nuevo_bono = bono(Año=año, Mes=mes, Quincena=quincena, Calificacion=calificacion, cal_empleado=empleado)
                nuevo_bono.save()

        # Redirigir al usuario a una página de confirmación
        return redirect('confirmacion_actualizacion')

    else:
        # Obtener todos los empleados para mostrar en el formulario
        todos_empleados = empleados.objects.all()
        form = BonoForm()

    return render(request, 'actualiza_calificacion.html', {'empleados': todos_empleados, 'form': form})

def confirmacion_actualizacion(request):
    # Esta vista podría mostrar un mensaje de éxito o alguna otra información relevante
    return render(request, 'confirmacion_actualizacion.html')

def produccion(request):
    return render(request, 'produccion.html')

def diseño(request):
    return render(request, 'diseño.html')

def ingenieriadeproducto(request):
    return render(request, 'ingenieria de producto.html')

def trazo(request):
    return render(request, 'trazo.html')

def corte(request):
    return render(request, 'corte.html')

def calidad(request):
    return render(request, 'calidad.html')

def almacenproducto(request):
    return render(request, 'almacen de producto.html')

def bordados(request):
    return render(request, 'bordados.html')

def embarques(request):
    return render(request, 'embarques.html')

def comprasinternacionales(request):
    return render(request, 'compras internacionales.html')

def comprasmateriaprima(request):
    return render(request, 'compras de materia prima.html')

def comprasproductoterminado(request):
    return render(request, 'compras producto terminado.html')

def diversion(request):
    return render(request, 'diversion.html')

def galeria(request):
    return render(request, 'galeria.html')

def descripcionesdepuesto(request):
    return render(request, 'descripciones de puesto.html')

def frases(request):
    return render(request, 'frases.html')

def reglamento(request):
    return render(request, 'reglamento interno.html')

def organigrama(request):
    return render(request, 'organigrama.html')

def macroproceso(request):
    return render(request, 'macroproceso.html')

def dcedicor(request):
    return render(request, 'cedicord.html')

def dcompras(request):
    return render(request, 'comprasd.html')

def vacaciones(request):
    return render(request, 'vacaciones.html')

def configuracion(request):
    return render(request, 'configuracion.html')
    
def avisop(request):
    return render(request, 'aviso de privacidad.html')

def inicio_portal(request):
    if request.user.is_authenticated:
        try:
            usuario = CorreosLazzar.objects.get(correo = request.user.email)
            return redirect('inicio')
        
        except CorreosLazzar.DoesNotExist:
            messages.warning(request, 'Tu número de empleado no es válido.')
            return redirect('intranet')

@login_required(login_url="login")
def vacation_days(request):
    if request.user.is_authenticated:
        try:
            usuario = CorreosLazzar.objects.get(correo=request.user.email)
            empleado = empleados.objects.get(codigo=usuario.num_empleado)
            vacaciones = dias_disponibles_vacaciones.objects.get(dato_empleado=empleado)
            programados = DiasProgramadasVacaciones.objects.filter(prog_empleado=empleado).order_by('fecha_inicio')

            colaboradores = empleados.objects.filter(codigo_jefe=usuario.num_empleado)
            col_vacaciones_list = []
            col_programados_list = []

            for colaborador in colaboradores:
                col_vacaciones = dias_disponibles_vacaciones.objects.get(dato_empleado__codigo=colaborador.codigo)
                col_vacaciones_list.append(col_vacaciones)

                col_programados = DiasProgramadasVacaciones.objects.filter(prog_empleado__codigo=colaborador.codigo).order_by('fecha_inicio')

                if col_programados.exists():
                    col_programados_list.append(col_programados)

            context = {
                'vacaciones': vacaciones,
                'programados': programados,
                'col_vacaciones_list': col_vacaciones_list,
                'col_programados_list': col_programados_list,
            }

        except CorreosLazzar.DoesNotExist:
            empleado = empleados.objects.get(codigo=request.user.username)
            vacaciones = dias_disponibles_vacaciones.objects.get(dato_empleado=empleado)
            programados = DiasProgramadasVacaciones.objects.filter(prog_empleado=empleado).order_by('fecha_inicio')

            try:
                colaboradores = empleados.objects.filter(codigo_jefe=empleado.codigo)
                col_vacaciones_list = []
                col_programados_list = []

                for colaborador in colaboradores:
                    col_vacaciones = dias_disponibles_vacaciones.objects.get(dato_empleado__codigo=colaborador.codigo)
                    col_vacaciones_list.append(col_vacaciones)

                    col_programados = DiasProgramadasVacaciones.objects.filter(prog_empleado__codigo=colaborador.codigo).order_by('fecha_inicio')

                    if col_programados.exists():
                        col_programados_list.append(col_programados)

                context = {
                    'vacaciones': vacaciones,
                    'programados': programados,
                    'col_vacaciones_list': col_vacaciones_list,
                    'col_programados_list': col_programados_list,
                }
            except empleados.DoesNotExist:
                context = {
                    'vacaciones': vacaciones,
                    'programados': programados,
                }

        return render(request, 'vacaciones.html', context)

    return redirect('login')
        
def programar_dias(request, empleado_id):
    empleado = empleados.objects.get(id=empleado_id)
    dias_disponibles = dias_disponibles_vacaciones.objects.get(dato_empleado=empleado)

    if request.method == 'POST':
        form = DiasProgramadasForm(request.POST)
        if form.is_valid():
            if dias_disponibles.saldo_final <= 0:
                messages.warning(request, 'No puedes programar más días de los disponibles')
                return redirect('vacation_days')

            # Definir fechas festivas - Mayer 15-02-2024
            holidays = ['2024-02-05', '2024-03-18', '2024-05-01', '2024-09-16', '2024-11-18', '2024-12-25', '2024-10-01']

            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_final = form.cleaned_data['fecha_final']

            # Lógica para calcular díasTotales y nuevoSaldo
            dias_totales = np.busday_count(fecha_inicio, fecha_final, holidays=holidays) + 1 # Excluye sábados, domingos y días festivos

            if dias_disponibles.saldo_final <= 4 and dias_totales > 5:
                messages.warning(request, 'No puedes programar más días de los disponibles')
                return redirect('vacation_days')

            programaciones = DiasProgramadasVacaciones.objects.filter(prog_empleado=empleado)
            for item in programaciones:
                fecha_inicio = item.fecha_inicio
                fecha_final = item.fecha_final

                dias = np.busday_count(fecha_inicio, fecha_final) + 1 # Excluye sábados y domingos
                dias_totales += dias

            dias_adicionales = math.floor(dias_totales // 5)
            dias_programados = dias_totales + dias_adicionales
            saldo = dias_disponibles.saldo_anterior + dias_disponibles.dias_vacaciones - dias_disponibles.semana_santa
            nuevo_saldo = saldo - dias_programados

            if nuevo_saldo < -1:
                messages.warning(request, 'No puedes programar más días de los disponibles')
                return redirect('vacation_days')
            
            elif nuevo_saldo >= -1 and dias_disponibles.saldo_final >= 5:
                # Actualizar saldo y días programados
                dias_disponibles.programados = dias_programados
                dias_disponibles.saldo_final = nuevo_saldo
                dias_disponibles.save()

                # Guardar la nueva programación de días
                dias_programadas = form.save(commit=False)
                dias_programadas.prog_empleado = empleado
                dias_programadas.save()

                return redirect('vacation_days')
            else:
                if  nuevo_saldo >= 0:
                    # Actualizar saldo y días programados
                    dias_disponibles.programados = dias_programados
                    dias_disponibles.saldo_final = nuevo_saldo
                    dias_disponibles.save()

                    # Guardar la nueva programación de días
                    dias_programadas = form.save(commit=False)
                    dias_programadas.prog_empleado = empleado
                    dias_programadas.save()
                else:
                    messages.warning(request, 'No puedes programar más días de los disponibles')
                    return redirect('vacation_days')
    else:
        form = DiasProgramadasForm()

    return redirect('vacation_days')

def eliminar_programacion(request, prog_id):
    if request.method == 'POST':
        programacion = get_object_or_404(DiasProgramadasVacaciones, id=prog_id)
        empleado = programacion.prog_empleado
        dias_disponibles = dias_disponibles_vacaciones.objects.get(dato_empleado=empleado)

        programacion.delete()

        dias_totales = 0
        dias_adicionales = 0

        programaciones = DiasProgramadasVacaciones.objects.filter(prog_empleado=empleado)
        for item in programaciones:
            fecha_inicio = item.fecha_inicio
            fecha_final = item.fecha_final

            dias = np.busday_count(fecha_inicio, fecha_final) + 1 # Excluye sábados y domingos
            dias_totales += dias

        dias_adicionales = math.floor(dias_totales // 5)
        dias_programados = dias_totales + dias_adicionales
        nuevo_saldo = dias_disponibles.saldo_anterior + dias_disponibles.dias_vacaciones - dias_disponibles.semana_santa - dias_programados

        # Actualizar saldo y días programados
        dias_disponibles.programados = dias_programados
        dias_disponibles.saldo_final = nuevo_saldo
        dias_disponibles.save()

    else:
        form = DiasProgramadasForm()

    return redirect('vacation_days')

def descarga_pdf(request, prog_id):
    if request.method == 'POST':
        programacion = get_object_or_404(DiasProgramadasVacaciones, id=prog_id)

        fecha = datetime.now().date()
        fecha_inicio = programacion.fecha_inicio
        fecha_final = programacion.fecha_final
        dias_totales = np.busday_count(fecha_inicio, fecha_final) + 1 # Excluye sábados y domingos
        empleado = programacion.prog_empleado
        nombre = empleado.apellido_materno + " " + empleado.apellido_paterno + " " + empleado.nombre
        puesto = empleado.puesto
        departamento = empleado.departamento
        archivo = "Vacaciones " + nombre + str(fecha_inicio) + ".pdf"
        
        context = {
                    'fecha_inicio': fecha_inicio,
                    'fecha_final': fecha_final,
                    'nombre': nombre,
                    'puesto': puesto,
                    'departamento': departamento,
                    'fecha': fecha,
                    'dias_totales': dias_totales,
                }
        
        #return render(request, 'Formato_de_Vacaciones_Lazzar.html', context)
        html_content = render_to_string('Formato_de_Vacaciones_Lazzar.html', context)
        pdf_content = pdfkit.from_string(html_content, False)

        # Configura la respuesta HTTP para descargar el archivo
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + archivo + '"'

        return response
    else:
        form = DiasProgramadasForm()

    return redirect('vacation_days')
    
@login_required(login_url="login")
def mostrar_bono(request):
    try:
        # Intentar obtener el usuario registrado en CorreosLazzar
        usuario_correos_lazzar = CorreosLazzar.objects.get(correo=request.user.email)
    
        # Si es un usuario registrado en CorreosLazzar, mostrar todos los bonos asociados a ese usuario
        bonos = bono.objects.filter(cal_empleado__codigo=usuario_correos_lazzar.num_empleado).order_by('-Año', '-Mes', '-Quincena')
        context = {
            'bonos': bonos,
            'usuario_correos_lazzar': usuario_correos_lazzar,
            'usuario_empleado': None,
        }

    except CorreosLazzar.DoesNotExist:
        try:
            # Intentar obtener el empleado asociado al usuario actual
            usuario_empleado = empleados.objects.get(codigo=request.user.username)

            # Si es un usuario de Empleados, mostrar los bonos solo para el empleado actual
            bonos = bono.objects.filter(cal_empleado=usuario_empleado).order_by('-Año', '-Mes', '-Quincena')
            context = {
                'bonos': bonos,
                'usuario_correos_lazzar': None,
                'usuario_empleado': usuario_empleado,
            }

        except empleados.DoesNotExist:
            # Si el usuario no es ni un usuario registrado en CorreosLazzar ni un empleado, redirigir a la página de inicio
            return redirect('login')

    return render(request, 'bono.html', context)