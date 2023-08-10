from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TutorRegistroForm, TutorInicioSesionForm, TutoradoRegistroForm, TutoradoInicioSesionForm, TutoriaIndividualForm
from .models import Tutor, Tutorado, TutoriaIndividual
from django.contrib import messages
from django.contrib.auth.hashers import check_password
# Create your views here.


def hello_world(request):
    return HttpResponse("Hola mundo")


def inicio(request):
    return render(request, 'inicio.html')


# Si la clave 'logged_in' no está presente en request.session, se asignará el valor False por defecto a la variable logged_in
def menu(request):
    # Obtiene el valor de 'logged_in' de la sesión, si no existe, se asigna False por defecto
    logged_in = request.session.get('logged_in', False)
    # Obtiene el valor de 'rol' de la sesión
    rol = request.session.get('rol')

    # Si el usuario está iniciado sesión y su rol es 'Tutor'
    if logged_in and rol == 'Tutor':
        # Obtiene el tutor que corresponde al número de empleado almacenado en la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])
        # Obtiene todas las tutorías individuales que tiene a su cargo el tutor
        tutorias_individuales = TutoriaIndividual.objects.filter(idTutor=tutor)
        # Renderiza la plantilla 'menuTutor.html' con el contexto
        return render(request, 'menuTutor.html', {'logged_in': logged_in,
                                                  'rol': rol,
                                                  'tutorias_individuales': tutorias_individuales})

    # Si el usuario está iniciado sesión y su rol es 'Tutorado'
    elif logged_in and rol == 'Tutorado':
        # Obtén el objeto Tutorado correspondiente al correo electrónico almacenado en la sesión
        tutorado = Tutorado.objects.get(
            boletaTutorado=request.session['boleta_tutorado'])

        # Recupera todas las tutorías individuales en las que está inscrito el Tutorado
        tutorias_inscritas = TutoriaIndividual.objects.filter(
            idTutorado=tutorado)

        # Renderiza la plantilla 'menuTutorado.html' con la información del usuario y las tutorías inscritas
        return render(request, 'menuTutorado.html', {'logged_in': logged_in,
                                                     'rol': rol,
                                                     'tutorias_inscritas': tutorias_inscritas})

    # Si el usuario no está iniciado sesión o su rol no coincide
    else:
        # Redirige al usuario a la vista 'inicio'
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
                # Checamos si la contraseña es correcta, solo que no sé que tan seguro sea hacerlo de esta forma, funciona pero no lo sé
                password = Tutorado.objects.get(password=password)
                request.session['logged_in'] = True
                request.session['rol'] = 'Tutorado'
                request.session['boleta_tutorado'] = boleta_tutorado
                return redirect('menu')

            except Tutorado.DoesNotExist:
                # Tutor no encontrado
                messages.error(request, 'Tutorado no encontrado.')

    else:
        form = TutoradoInicioSesionForm()

    return render(request, 'inicioSesionTutorado.html', {'form': form})


def cerrar_sesion(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('inicio')


def crear_tutoria_individual(request):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    if request.method == 'POST':
        form = TutoriaIndividualForm(request.POST)
        if form.is_valid():
            # Obtiene el tutor de la sesión
            tutor = Tutor.objects.get(
                numeroEmpleado=request.session['numero_empleado'])
            tutoria_individual = form.save(commit=False)

            # Verifica si el Tutorado tiene menos de 3 tutores asignados
            tutorado = tutoria_individual.idTutorado
            if tutorado.numTutoresAsignados < 3:
                # Asigna el tutor a la instancia de tutoría individual
                tutoria_individual.idTutor = tutor
                # Guarda la instancia de tutoría individual en la BD
                tutoria_individual.save()

                # Incrementa el campo numTutoresAsignados del Tutorado en una unidad
                tutorado.numTutoresAsignados += 1
                tutorado.save()

                # Redirige a la vista 'menu'
                return redirect('menu')
            else:
                # Muestra un mensaje de error si el Tutorado ya tiene 3 tutores asignados
                messages.error(
                    request, 'El Tutorado ya está inscrito en 3 tutorías.')
    else:  # GET
        form = TutoriaIndividualForm()

    # Agrega las variables logged_in y rol al contexto

    # Estamos creando un diccionario llamado context que contiene varias variables que se pasarán como contexto a la plantilla crearTutoriaIndividual.html cuando se renderice

    # El contexto es simplemente un conjunto de variables que se utilizan para mostrar información en la plantilla.
    context = {'form': form, 'logged_in': logged_in, 'rol': rol}
    return render(request, 'crearTutoriaIndividual.html', context)
