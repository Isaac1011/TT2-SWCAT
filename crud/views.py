from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TutorRegistroForm, TutorInicioSesionForm, TutoradoRegistroForm, TutoradoInicioSesionForm
from .models import Tutor, Tutorado
from django.contrib import messages
from django.contrib.auth.hashers import check_password

# Create your views here.


def hello_world(request):
    return HttpResponse("Hola mundo")


def inicio(request):
    return render(request, 'inicio.html')


# Si la clave 'logged_in' no está presente en request.session, se asignará el valor False por defecto a la variable logged_in
def menu(request):
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    if logged_in and rol == 'Tutor':
        return render(request, 'menuTutor.html', {'logged_in': logged_in,
                                                  'rol': rol})
    elif logged_in and rol == 'Tutorado':
        return render(request, 'menuTutorado.html', {'logged_in': logged_in,
                                                     'rol': rol})
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
            request.session['rol'] = 'Tutor'
            request.session['numero_empleado'] = numero_empleado
            return redirect('menu')
    else:  # GET
        form = TutorRegistroForm()
    return render(request, 'registroTutor.html', {
        'form': form
    })


def registro_tutorado(request):
    if request.method == 'POST':
        form = TutoradoRegistroForm(request.POST)
        if form.is_valid():
            boleta_tutorado = form.cleaned_data['boletaTutorado']
            form.save()
            # Inicio de sesión exitoso
            request.session['logged_in'] = True
            request.session['rol'] = 'Tutorado'
            request.session['boleta_tutorado'] = boleta_tutorado
            return redirect('menu')
    else:  # GET
        form = TutoradoRegistroForm()
    return render(request, 'registroTutorado.html', {
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
                    request.session['rol'] = 'Tutor'
                    request.session['numero_empleado'] = numero_empleado

                    # Reemplaza con la URL que deseas redireccionar
                    return redirect('menu')
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


def inicio_sesion_tutorado(request):
    if request.method == 'POST':
        form = TutoradoInicioSesionForm(request.POST)
        if form.is_valid():
            boleta_tutorado = form.cleaned_data['boletaTutorado']
            password = form.cleaned_data['password']

            # Verificar si las credenciales son válidas
            try:
                tutorado = Tutorado.objects.get(boletaTutorado=boleta_tutorado)
                if check_password(password, tutorado.password):
                    # Inicio de sesión exitoso
                    request.session['logged_in'] = True
                    request.session['rol'] = 'Tutorado'
                    request.session['boleta_tutorado'] = boleta_tutorado

                    # Reemplaza con la URL que deseas redireccionar
                    return redirect('menu')
                else:
                    # Credenciales inválidas
                    messages.error(
                        request, 'Credenciales inválidas. Inténtalo de nuevo.')
            except Tutorado.DoesNotExist:
                # Tutor no encontrado
                messages.error(request, 'Tutorado no encontrado.')

    else:
        form = TutoradoInicioSesionForm()

    return render(request, 'inicioSesionTutorado.html', {'form': form})


# Funciona correctamente para proteger las rutas, pero no elimina la cookie 'sessionid' del navegador
def cerrar_sesion(request):
    if 'logged_in' in request.session:
        del request.session['logged_in']
        del request.session['rol']
    if 'numero_empleado' in request.session:
        del request.session['numero_empleado']
    if 'boleta_tutorado' in request.session:
        del request.session['boleta_tutorado']
    return redirect('inicio')
