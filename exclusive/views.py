from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth.models import User
from intranet.models import empleados
from django.shortcuts import render

def registro(request): #-- Request Registrar Usuario -- 
    if request.user.is_authenticated:
        return redirect('inicio-exclusive')
    else:
        register_form = RegisterForm()

        if request.method == 'POST':
            register_form = RegisterForm(request.POST)

            # Obetenemos el correo capturado
            correo_ingresado = request.POST['email']

            try:
                # Verifica que el corro este en la lista de correos permitidos
                new_user = empleados.objects.get(correo = correo_ingresado)

                # Obetenemos el correo de la lista
                registered_user = new_user.correo

                try:
                    # Verifica que el corro no este en uso o es de otro usuario
                    User.objects.get(email = registered_user)
                    messages.success(request, 'El correo ya esta registrado')

                # Si no esta en uso o no pertenece a otor usuario
                except User.DoesNotExist:

                    if register_form.is_valid():
                        user = register_form.save()
                        messages.success(request, 'Te has registrado correctamente (: ')
                        return redirect('index-exclusive')
            
            # Si el correo no esta en la lista de correos permitidos
            except empleados.DoesNotExist:
                messages.warning(request, 'Tu cuenta de correo no es valida.')

                return render(request, 'registro.html',{
                    'title': 'Registro',
                    'register_form': register_form
                })
            
        return render(request, 'registro.html',{
            'title': 'Registro',
            'register_form': register_form
        })

def login_page(request):
    if request.user.is_authenticated:
        return redirect('index-exclusive')  
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                grupo_user = User.objects.get(username=username)
                usuario = empleados.objects.get(correo=grupo_user.email)

                # función redirect() para redirigir a la URL con nombre 'inicio' Jesús Ibarra 19/12/2023
                return redirect('index-exclusive')
            else:
                messages.warning(request, 'Favor de verificar tu usuario y contraseña.')

        return render(request, 'login.html', {
            'title': 'Iniciar Sesión',
        })
    
def index_exclusive(request):


    return render(request, 'index-exclusive.html')
