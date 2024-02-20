from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, Respuesta, Tecnico
from .forms import *
from django.db.models import OuterRef, Subquery, Max, Count, Value
from django.db.models.functions import Coalesce
from django.contrib.auth.models import Group
from email.mime.text import MIMEText
from mainapp.models import CorreosLazzar
import smtplib

@login_required
def listar_tickets(request):
    usuario_log = request.user.username
    soporte = request.user.groups.filter(name='Soporte').exists()
    admin = False
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups

    if (soporte):
        admin = request.user.groups.filter(name='admin_soporte').exists()

        if(admin):
            tickets = Ticket.objects.annotate(
                fecha_ultima_respuesta=Coalesce(
                    Subquery(
                        Respuesta.objects.filter(ticket=OuterRef('pk')).order_by('-fecha_respuesta').values('fecha_respuesta')[:1]
                    ), 
                    Value(None)
                    )
                ).values('folio', 'asunto','fecha_alta','fecha_ultima_respuesta','estatus', 'tecnico').order_by('-folio')
            
        else:
            tickets = Ticket.objects.annotate(
                fecha_ultima_respuesta=Coalesce(
                    Subquery(
                        Respuesta.objects.filter(ticket=OuterRef('pk')).order_by('-fecha_respuesta').values('fecha_respuesta')[:1]
                    ), 
                    Value(None)
                    )
                ).values('folio', 'asunto','fecha_alta','fecha_ultima_respuesta','estatus').order_by('-folio')

        return render(request, 'listar_tickets.html', 
                    {
                        'tickets': tickets, 
                        'usuario_log': usuario_log,
                        'admin': admin,
                        'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                        'acceso_total': acceso_total,
                        'mesa_control': mesa_control, # End Admin-Groups
                    })
        
    else:
        tickets = Ticket.objects.annotate(
        fecha_ultima_respuesta=Coalesce(
            Subquery(
                Respuesta.objects.filter(ticket=OuterRef('pk')).order_by('-fecha_respuesta').values('fecha_respuesta')[:1]
            ), 
            Value(None)
            )
        ).filter(usuario=request.user.id).values('folio', 'asunto','fecha_alta','fecha_ultima_respuesta','estatus').order_by('-folio')
    
        return render(request, 'listar_tickets.html', 
            {
                'tickets': tickets,
                'usuario_log': usuario_log,
                'admin':admin,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })

@login_required
def detalle_ticket(request, ticket_id):
    usuario_log = request.user.username
    soporte = request.user.groups.filter(name='Soporte').exists()
    
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    form = RespuestaForm()

    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups

    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta_texto = form.cleaned_data['respuesta_texto']
            ticket.agregar_respuesta(request.user.tecnico, respuesta_texto)
            return redirect('detalle_ticket', ticket_id=ticket.id)

    return render(request, 'detalle_ticket.html', 
            {
                'ticket': ticket, 
                'form': form,
                'usuario_log': usuario_log,
                'soporte':soporte,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })

@login_required
def agregar_respuesta(request, ticket_id):
    ticket = Ticket.objects.get(folio=ticket_id)
    name_tecnico = Tecnico.objects.filter(usuario_id=request.user.id)
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups
    
    if request.method == 'POST':
        form = RespuestaForm(request.POST, request.FILES)
        tecnico_id = request.POST.get('tecnico_id')
        tecnico = Tecnico.objects.get(id=tecnico_id)
        
        if form.is_valid():
            respuesta_texto = form.cleaned_data['respuesta_texto']
            adjuntos_res = form.cleaned_data['adjuntos_res']
            if len(name_tecnico) == 0:
                us_resp = User.objects.get(id=request.user.id)
                ticket.agregar_respuesta(None, respuesta_texto, adjuntos_res, us_resp)
            else:
                ticket.agregar_respuesta(name_tecnico[0], respuesta_texto, adjuntos_res,None)

            ticket2 = Ticket.objects.get(pk=ticket_id)
            
            correo_respuesta(ticket2,ticket2.usuario.email, ticket2.tecnico.correo_tec)

            return redirect('detalle_ticket', ticket_id=ticket.folio)

    else:
        form = RespuestaForm()

    return render(request, 'agregar_respuesta_form.html', {
        'form': form, 
        'ticket': ticket,
        'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
        'acceso_total': acceso_total,
        'mesa_control': mesa_control, # End Admin-Groups
        })

@login_required
def crear_ticket(request):
    usuario_log = request.user.username
    correo_user = request.user.email
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.usuario = request.user
            ticket.save()

            enviar_correo(ticket, correo_user, None)

            return redirect('detalle_ticket', ticket_id=ticket.folio)
    else:
        form = TicketForm()

    return render(request, 'crear_ticket.html', 
                {'form': form,
                 'usuario_log': usuario_log,
                 'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                 'acceso_total': acceso_total,
                 'mesa_control': mesa_control, # End Admin-Groups
                })

def enviar_correo(ticket, correo_user, correo_tec):
    # Configura tus credenciales y detalles del servidor SMTP de Gmail
    correo_emisor = 'sistemas@lazzarmexico.com'
    contraseña = 'nldflybxyeiukvko'
    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587
    
    # Construye el cuerpo del correo electrónico
    asunto = f"Nuevo ticket creado - {ticket.asunto}"
    mensaje = f"Se ha creado un nuevo ticket con asunto: {ticket.asunto}\nDescripción: {ticket.descripcion}\nFolio: {ticket.folio}"

    # Configura el correo electrónico

    if correo_tec == None:
        msg = MIMEText(mensaje)
        msg['Subject'] = asunto
        msg['From'] = correo_emisor
        msg['To'] = correo_emisor  # Reemplaza con la dirección de correo del destinatario
        
    else:
        msg = MIMEText(mensaje)
        msg['Subject'] = asunto
        msg['From'] = correo_emisor
        msg['To'] = correo_user  # Reemplaza con la dirección de correo del destinatario
        msg['Cc'] = correo_tec
        msg['Cco'] = correo_tec

    # Conecta y autentica con el servidor SMTP de Gmail
    server = smtplib.SMTP(servidor_smtp, puerto_smtp)
    server.starttls()
    server.login(correo_emisor, contraseña)

    if correo_tec == None:
        # Envía el correo electrónico
        server.sendmail(correo_emisor, 'sistemas@lazzarmexico.com', msg.as_string())
    else:
        # Envía el correo electrónico
        server.sendmail(correo_emisor, [correo_user, correo_tec, 'sistemas@lazzarmexico.com'], msg.as_string())

    # Cierra la conexión con el servidor SMTP
    server.quit()

@login_required
def asignar_ticket(request, ticket_id):
    usuario_log = request.user.username
    #ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket = Ticket.objects.get(pk=ticket_id)
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups

    if request.method == 'POST':
        form = Aisgna_TecnicoForm(request.POST,instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            form.save()
            
            ticket2 = Ticket.objects.get(pk=ticket_id)
            
            enviar_correo(ticket2,ticket2.usuario.email, ticket2.tecnico.correo_tec)

            return redirect('detalle_ticket', ticket_id=ticket.folio)
    else:
        form = Aisgna_TecnicoForm(instance=ticket)

    return render(request, 'asignar_ticket.html',{
        'form': form,
        'ticket': ticket,
        'usuario_log': usuario_log,
        'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
        'acceso_total': acceso_total,
        'mesa_control': mesa_control, # End Admin-Groups
    })

@login_required
def cambia_status(request, ticket_id):
    usuario_log = request.user.username
    name_tecnico = Tecnico.objects.filter(usuario_id=request.user.id)
    ticket = Ticket.objects.get(pk=ticket_id)
    ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
    acceso_total = request.user.groups.filter(name='acceso_total').exists()
    mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups

    if request.method == 'POST':
        form = status(request.POST,instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            form.save()

            ticket2 = Ticket.objects.get(pk=ticket_id)
            
            correo_estatus(ticket2,ticket2.usuario.email, ticket2.tecnico.correo_tec)

            return redirect('detalle_ticket', ticket_id=ticket.folio)
    else:
        form = status(instance=ticket)

    return render(request, 'detalle_ticket.html',{
        'form': form,
        'ticket': ticket,
        'usuario_log': usuario_log,
        'name_tecnico':name_tecnico[0],
        'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
        'acceso_total': acceso_total,
        'mesa_control': mesa_control, # End Admin-Groups
    })

def correo_estatus(ticket, correo_user, correo_tec):
    # Configura tus credenciales y detalles del servidor SMTP de Gmail
    correo_emisor = 'sistemas@lazzarmexico.com'
    contraseña = 'nldflybxyeiukvko'
    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587
    
    # Construye el cuerpo del correo electrónico
    asunto = f"Tu solicitud # {ticket.folio} cambio"
    mensaje = f"Tu solicitud con asunto: {ticket.asunto}\nDescripción: {ticket.descripcion}\nFolio: {ticket.folio}\nCambio de estatus a: {ticket.estatus}"

    # Configura el correo electrónico
    msg = MIMEText(mensaje)
    msg['Subject'] = asunto
    msg['From'] = correo_emisor
    msg['To'] = correo_user  # Reemplaza con la dirección de correo del destinatario
    msg['Cc'] = correo_tec
    msg['Cco'] = correo_tec

    # Conecta y autentica con el servidor SMTP de Gmail
    server = smtplib.SMTP(servidor_smtp, puerto_smtp)
    server.starttls()
    server.login(correo_emisor, contraseña)

    # Envía el correo electrónico
    server.sendmail(correo_emisor, [correo_user, correo_tec, 'sistemas@lazzarmexico.com'], msg.as_string())

    # Cierra la conexión con el servidor SMTP
    server.quit()

def correo_respuesta(ticket, correo_user, correo_tec):
    # Configura tus credenciales y detalles del servidor SMTP de Gmail
    correo_emisor = 'sistemas@lazzarmexico.com'
    contraseña = 'nldflybxyeiukvko'
    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587
    
    # Construye el cuerpo del correo electrónico
    respuestas = Respuesta.objects.filter(ticket_id=ticket.folio).order_by('-fecha_respuesta').first()

    asunto = f"Tu solicitud # {ticket.folio} tiene una nueva respuesta"
    mensaje = f"Tu solicitud con asunto: {ticket.asunto}\nDescripción: {ticket.descripcion}\nFolio: {ticket.folio}\nTiene una nueva respuesta: \n{respuestas.respuesta_texto}"

    # Configura el correo electrónico
    msg = MIMEText(mensaje)
    msg['Subject'] = asunto
    msg['From'] = correo_emisor
    msg['To'] = correo_user  # Reemplaza con la dirección de correo del destinatario
    msg['Cc'] = correo_tec
    msg['Cco'] = correo_tec

    # Conecta y autentica con el servidor SMTP de Gmail
    server = smtplib.SMTP(servidor_smtp, puerto_smtp)
    server.starttls()
    server.login(correo_emisor, contraseña)

    # Envía el correo electrónico
    server.sendmail(correo_emisor, [correo_user, correo_tec, 'sistemas@lazzarmexico.com'], msg.as_string())

    # Cierra la conexión con el servidor SMTP
    server.quit()
