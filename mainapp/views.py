from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.forms import RegisterForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import path

from django.contrib.auth.models import Group
from django.contrib.auth.models import User, Group
from mainapp.models import CorreosLazzar
from django.shortcuts import render
from intranet.models import empleados

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView

# Create your views here.

# Mayer Orozco 22/01/2024 Validación del registro, con la BD de Correo y Empleados
def verificar_correo_y_empleado(request, register_form, correo_ingresado, user_name, apellidos):
    try:
        new_user = CorreosLazzar.objects.get(correo=correo_ingresado)
        registered_user = new_user.correo

        try:
            User.objects.get(email=registered_user)
            messages.success(request, 'El correo ya está registrado')
            return False

        except User.DoesNotExist:
            try:
                if user_name.isdigit():   
                    empleados.objects.get(codigo=user_name)
                    if register_form.is_valid():
                        user = register_form.save()
                        messages.success(request, 'Te has registrado correctamente (: ')
                        return True
                else:
                    if register_form.is_valid():
                        user = register_form.save()
                        messages.success(request, 'Te has registrado correctamente (: ')
                        return True
                
                messages.warning(request, 'Tu número de empleado no es válido.')
                return False

            except empleados.DoesNotExist:
                messages.warning(request, 'Tu número de empleado no es válido.')

    except CorreosLazzar.DoesNotExist:
        try:
            if user_name.isdigit():
                CorreosLazzar.objects.get(num_empleado=user_name)
                messages.success(request, 'Tu número de empleado ya está registrado')
                return False
            
            messages.warning(request, 'Tu número de empleado no es válido.')
            return False

        except CorreosLazzar.DoesNotExist:
            try:
                apellido = apellidos.split()
                empleados.objects.get(codigo=user_name, apellido_paterno=apellido[0])
                
                if register_form.is_valid():
                    user = register_form.save()
                    messages.success(request, 'Te has registrado correctamente (: ')
                    return True

            except empleados.DoesNotExist:
                messages.warning(request, 'Tu número o apellidos de empleado no son válidos')

    return False

# Mayer Orozco 22/01/2024 Nuevo registrer_page
def registrer_page(request):
    # Si ya esta logueado lo manda a inicio
    if request.user.is_authenticated:
        return redirect('inicio')
    else:
        register_form = RegisterForm()

        if request.method == 'POST':
            register_form = RegisterForm(request.POST)

            #obtiene el Correo, Username, Apelldios
            correo_ingresado = request.POST['email']
            user_name = request.POST['username']
            apellidos = request.POST['last_name']

            #Valida si le esta permitido crear un registro con la BD Correo y Empleados
            if verificar_correo_y_empleado(request, register_form, correo_ingresado, user_name, apellidos):
                return redirect('inicio')

        return render(request, 'users/register.html', {
            'title': 'Registro',
            'register_form': register_form
        })
    
    # Mayer Orozco 22/01/2024 Se reemplaza por el nuevo registrer_page
""" def registrer_page(request): #-- Request Registrar Usuario -- 
    if request.user.is_authenticated:
        return redirect('inicio')
    else:
        register_form = RegisterForm()

        if request.method == 'POST':
            register_form = RegisterForm(request.POST)

            # Obetenemos el correo capturado
            correo_ingresado = request.POST['email']

            try:
                # Verifica que el corro este en la lista de correos permitidos
                new_user = CorreosLazzar.objects.get(correo = correo_ingresado)

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
                        return redirect('index')

                    """ """ Verificar el dominio del correo electrónico para asignar el grupo correspondiente
                     email = user.email
                    if email.endswith('@gmail.com'):
                        # Asignar al grupo con acceso total
                        group = Group.objects.get(name='acceso_total')
                    elif email.endswith('@hotmail.com'):
                        # Asignar al grupo de ventas
                        group = Group.objects.get(name='ventas')

                    user.groups.add(group) """ """
            
            # Si el correo no esta en la lista de correos permitidos
            except CorreosLazzar.DoesNotExist:
                messages.warning(request, 'Tu cuenta de correo no es valida.')

                return render(request, 'users/register.html',{
                    'title': 'Registro',
                    'register_form': register_form
                })
            
        return render(request, 'users/register.html',{
            'title': 'Registro',
            'register_form': register_form
        }) """
    
class PasswordResetCustomView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/reset_email.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/resetdone.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'users/reset.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/complete.html'

# Mayer Orozco 22/01/2024 Nuevo login_page
def login_page(request):
    if request.user.is_authenticated:
        return redirect('inicio')  # Redirige a la URL con nombre 'inicio'
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                try:
                    login(request, user)
                    grupo_user = User.objects.get(username=username)
                    usuario = CorreosLazzar.objects.get(correo=grupo_user.email)

                    # función redirect() para redirigir a la URL con nombre 'inicio' Jesús Ibarra 19/12/2023
                    return redirect('inicio')
                except CorreosLazzar.DoesNotExist:
                    empleado = empleados.objects.get(codigo=username)
                    # Cinado intranet este listo cambiar el return intranet
                    #return redirect('vacation_days', 0)
                    return redirect('login-exclusive')

            else:
                messages.warning(request, 'Favor de verificar tu usuario y contraseña.')

        return render(request, 'users/login.html', {
            'title': 'Iniciar Sesión',
        })
    
    # Mayer Orozco 22/01/2024 Se reemplaza por el nuevo login_page
""" def login_page(request):
    if request.user.is_authenticated:
        return redirect('inicio')  # Redirige a la URL con nombre 'inicio'
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
            
                grupo_user = User.objects.get(username=username)
                usuario = CorreosLazzar.objects.get(correo=grupo_user.email)

                # función redirect() para redirigir a la URL con nombre 'inicio' Jesús Ibarra 19/12/2023
                return redirect('inicio')
            else:
                messages.warning(request, 'Favor de verificar tu usuario y contraseña.')

        return render(request, 'users/login.html', {
            'title': 'Iniciar Sesión',
        }) """

def index(request): #--Logica Index acceso total --
    if request.user.is_authenticated:
        try:
            usuario = CorreosLazzar.objects.get(correo = request.user.email)
            ventas = request.user.groups.filter(name='ventas').exists() #Admin-Groups Jesus Ibarra 19/12/2023
            acceso_total = request.user.groups.filter(name='acceso_total').exists()
            mesa_control = request.user.groups.filter(name='mesa_control').exists() # End Admin-Groups

            return render(request, 'index.html',{
                'title': 'Inicio',
                'usuario':usuario,
                'ventas': ventas, #Admin-Groups Jesus Ibarra 19/12/2023
                'acceso_total': acceso_total,
                'mesa_control': mesa_control, # End Admin-Groups
            })
        except CorreosLazzar.DoesNotExist: #Se agrego validación de correos lazzar y empleados para redirigir a su pagina correspondiente / Jesús Ibarra 29/ENERO/2024
            try:
                colaborador = empleados.objects.get(correo_nomina=request.user.email)
                return redirect('index-exclusive')
            except empleados.DoesNotExist:
                return render(request, 'index.html',{
                    'title': 'Inicio',
                }) #------------------------------------------------------------------------------------------------------------------------------------------------.
            
    return render (request, 'index.html')



def index_ventas(request): #reenderiza menu ventas y acceso total
    user = request.user
    is_acceso_total = user.groups.filter(name='acceso_total').exists()
    is_ventas = user.groups.filter(name='ventas').exists()

    context = {
        'is_acceso_total': is_acceso_total,
        'is_ventas': is_ventas
    }

    return render(request, 'users/index_ventas.html', {
    'title': 'Inicio',
    'is_acceso_total': is_acceso_total,
    'is_ventas': is_ventas
})

def search(request): #-- Opcion Buscado Boton
    if request.method == 'GET':
        query = request.GET.get('query', '').lower()  # Obtener el valor ingresado en el campo de búsqueda
        submit_value = request.GET.get('submit', '').lower().replace(" ", "")  # Obtener el valor del botón de búsqueda y eliminar espacios

        if 'bordados' in query and submit_value == 'bordados':
            return redirect('pedidos')  # Redirigir a la página de pedidos si el botón de búsqueda es 'Bordados' y la palabra 'bordados' está en la búsqueda
        elif 'estatus' in query and submit_value == 'estatus':
            return redirect('estatus_mesa')  # Redirigir a la página de estatus interno si el botón de búsqueda es 'Estatus Interno' y la palabra 'estatusinterno' está en la búsqueda
        elif 'nosotros' in query and submit_value == 'nosotros':
            return redirect('nosotros')  # Redirigir a la página de nosotros si el botón de búsqueda es 'Sobre Nosotros' y la palabra 'sobrenosotros' está en la búsqueda

    # Si no coincide ninguna palabra clave o no se ha enviado una búsqueda, renderiza la página normalmente
    return render(request, 'index.html')


def logout_user(request): #-- Request Cerrar Sesión -- 
    logout(request)
    return redirect('index')