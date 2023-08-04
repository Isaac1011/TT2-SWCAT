from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TutorRegistroForm, TutorInicioSesionForm
from .models import Tutor
from django.contrib import messages
from django.contrib.auth.hashers import check_password

# Create your views here.


def hello_world(request):
    return HttpResponse("Hola mundo")


def inicio(request):
    return render(request, 'inicio.html')


# Si la clave 'logged_in' no está presente en request.session, se asignará el valor False por defecto a la variable logged_in
def menu_tutor(request):
    logged_in = request.session.get('logged_in', False)

    if logged_in:
        return render(request, 'menuTutor.html', {'logged_in': logged_in})
    else:
        return redirect('inicio')


def registro_tutor(request):
    if request.method == 'POST':
        form = TutorRegistroForm(request.POST)
        if form.is_valid():
            numero_empleado = form.cleaned_data['numeroEmpleado']
            form.save()
            # Inicio de sesión exitoso
            request.session['logged_in'] = True
            request.session['numero_empleado'] = numero_empleado
            return redirect('menu_tutor')
    else:  # GET
        form = TutorRegistroForm()
    return render(request, 'registroTutor.html', {
        'form': form
    })


def inicio_sesion_tutor(request):
    if request.method == 'POST':
        form = TutorInicioSesionForm(request.POST)
        if form.is_valid():
            numero_empleado = form.cleaned_data['numeroEmpleado']
            password = form.cleaned_data['password']

            # Verificar si las credenciales son válidas
            try:
                tutor = Tutor.objects.get(numeroEmpleado=numero_empleado)
                if check_password(password, tutor.password):
                    # Inicio de sesión exitoso
                    request.session['logged_in'] = True
                    request.session['numero_empleado'] = numero_empleado

                    # Reemplaza con la URL que deseas redireccionar
                    return redirect('menu_tutor')
                else:
                    # Credenciales inválidas
                    messages.error(
                        request, 'Credenciales inválidas. Inténtalo de nuevo.')
            except Tutor.DoesNotExist:
                # Tutor no encontrado
                messages.error(request, 'Tutor no encontrado.')

    else:
        form = TutorInicioSesionForm()

    return render(request, 'inicioSesionTutor.html', {'form': form})


# Funciona correctamente para proteger las rutas, pero no elimina la cookie 'sessionid' del navegador


def cerrar_sesion_tutor(request):
    if 'logged_in' in request.session:
        del request.session['logged_in']
    if 'numero_empleado' in request.session:
        del request.session['numero_empleado']

    return redirect('inicio')
