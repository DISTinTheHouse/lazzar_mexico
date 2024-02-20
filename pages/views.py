from django.shortcuts import render, redirect
from .models import Page
from django.contrib.auth.decorators import login_required
from mainapp.models import CorreosLazzar
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import traceback

@login_required(login_url="login")
def page(request, slug):
    page = Page.objects.get(slug=slug)

    return render(request, "pages/page.html",{
        "page": page
    })

@login_required(login_url="login")
def nosotros(request):
    usuario = CorreosLazzar.objects.get(correo = request.user.email)

    return render(request, 'nosotros.html',{
        'title':'Sobre nosotros',
        'leyenda':False,
        'usuario': usuario
    })

def enviar_correo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        descripcion = request.POST.get('descripcion')

        try:
            send_mail(
                'Contacto desde el sitio web',
                f'Nombre: {nombre}\nCorreo: {correo}\nDescripción: {descripcion}',
                settings.EMAIL_HOST_USER,
                ['desarrollo@lazzarmexico.com'],
                fail_silently=False,
            )
            print("Correo enviado exitosamente")
        except Exception as e:
            print("Error al enviar el correo:")
            print(traceback.format_exc())

        messages.success(request, 'Tu mensaje ha sido enviado con éxito. Te contactaremos pronto.')

        return redirect('nosotros')

    return redirect('nosotros')
