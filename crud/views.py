from .forms import BitacoraIndividualTutorForm
from .models import BitacoraIndividualTutor
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import TutorRegistroForm, TutorInicioSesionForm, TutoradoRegistroForm, TutoradoInicioSesionForm, TutoriaIndividualForm, BitacoraIndividualTutorForm, NotasIndividualesTutoradoForm, TutoriaGrupalForm
from .models import Tutor, Tutorado, TutoriaIndividual, BitacoraIndividualTutor, NotasIndividualesTutorado, TutoriaGrupal
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
        # Obtiene todas las tutorías grupales que tiene a su cargo el tutor
        tutorias_grupales = TutoriaGrupal.objects.filter(idTutor=tutor)
        # Renderiza la plantilla 'menuTutor.html' con el contexto
        return render(request, 'tutor/menuTutor.html',
                      {'logged_in': logged_in,
                       'rol': rol,
                       'tutorias_individuales': tutorias_individuales,
                       'tutorias_grupales': tutorias_grupales}
                      )

    # Si el usuario está iniciado sesión y su rol es 'Tutorado'
    elif logged_in and rol == 'Tutorado':
        # Obtén el objeto Tutorado correspondiente al correo electrónico almacenado en la sesión
        tutorado = Tutorado.objects.get(
            boletaTutorado=request.session['boleta_tutorado'])

        # Recupera todas las tutorías individuales en las que está inscrito el Tutorado
        tutorias_inscritas = TutoriaIndividual.objects.filter(
            idTutorado=tutorado)

        # Renderiza la plantilla 'menuTutorado.html' con la información del usuario y las tutorías inscritas
        return render(request, 'tutorado/menuTutorado.html',
                      {'logged_in': logged_in,
                       'rol': rol,
                       'tutorias_inscritas': tutorias_inscritas}
                      )

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
    return render(request, 'tutor/registroTutor.html', {
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
    return render(request, 'tutorado/registroTutorado.html', {
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

    return render(request, 'tutor/inicioSesionTutor.html', {'form': form})


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

    return render(request, 'tutorado/inicioSesionTutorado.html', {'form': form})


def cerrar_sesion(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('inicio')


def crear_tutoriaIndividual(request):
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
    return render(request, 'tutor/tutoriaIndividual/crearTutoriaIndividual.html', context)


def detalle_tutoriaIndividual(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si NO estás logeado Y  no eres un Tutor or un Tutorado, redirige al inicio.
    # Con esto protejo la ruta menu/notaTutorIndividual/
    if (not logged_in) and (rol != 'Tutor' or rol != 'Tutorado'):
        return redirect('inicio')

    else:
        # Obtener la instancia de TutoriaIndividual según el ID proporcionado
        tutoria_individual = get_object_or_404(
            TutoriaIndividual, pk=tutoria_id)

        # Obtener las notas de la bitácora asociadas a esta tutoría individual
        notas_tutor = BitacoraIndividualTutor.objects.filter(
            idTutoriaIndividual=tutoria_individual)

        # Obtener las notas del tutorado asociadas a esta tutoría individual
        notas_tutorado = NotasIndividualesTutorado.objects.filter(
            idTutoriaIndividual=tutoria_individual)

        # Renderizar el template de detalle_tutoria.html con la instancia de tutoría individual
        context = {
            'tutoria_individual': tutoria_individual,
            'notas_tutor': notas_tutor,
            'notas_tutorado': notas_tutorado,
            'logged_in': logged_in,
            'rol': rol
        }
        return render(request, 'detalleTutoriaIndividual.html', context)


def bitacora_tutor_tutoriaIndividual(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    # Con esto protejo la ruta menu/notaTutorIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    # Obtén la instancia de la tutoría individual usando el ID proporcionado
    try:
        # Obtener la instancia de TutoriaIndividual según el ID proporcionado
        tutoria_individual = get_object_or_404(
            TutoriaIndividual, pk=tutoria_id)
    except TutoriaIndividual.DoesNotExist:
        # Manejo si la tutoría no existe
        messages.error(
            request, 'Tutor no encontrado.')
        # return redirect('inicio')

    if request.method == 'POST':
        form = BitacoraIndividualTutorForm(request.POST)
        if form.is_valid():
            # Crea una nueva instancia de BitacoraIndividualTutor, pero aún no la guarda en la base de datos
            bitacora = form.save(commit=False)
            bitacora.idTutoriaIndividual = tutoria_individual  # Asigna la tutoría individual
            bitacora.save()  # Ahora sí, guarda en la base de datos

            # Redirige a donde quieras después de registrar la nota
            # Cambia esto por la ruta adecuada
            return redirect('detalle_tutoriaIndividual', tutoria_id=tutoria_id)
    else:
        form = BitacoraIndividualTutorForm()

    context = {
        'form': form,
        'tutoria_individual': tutoria_individual,
        'logged_in': logged_in,
        'rol': rol
    }
    return render(request, 'tutor/tutoriaIndividual/crearBitacoraTutoriaIndividual.html', context)


def nota_tutorado_tutoriaIndividual(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    # Con esto protejo la ruta menu/notaTutorIndividual/
    if not logged_in or rol != 'Tutorado':
        return redirect('inicio')

    try:
        # Obtener la instancia de la tutoría individual según el ID proporcionado
        tutoria_individual = get_object_or_404(
            TutoriaIndividual, pk=tutoria_id)
    except TutoriaIndividual.DoesNotExist:
        # Manejo si la tutoría no existe
        messages.error(
            request, 'Tutoría no encontrada.')
        # return redirect('inicio')

    if request.method == 'POST':
        form = NotasIndividualesTutoradoForm(request.POST)
        if form.is_valid():
            # Crear una instancia de NotasIndividualesTutorado pero no guardarla aún
            nota = form.save(commit=False)
            nota.idTutoriaIndividual = tutoria_individual
            nota.save()
            return redirect('detalle_tutoriaIndividual', tutoria_id=tutoria_id)
    else:
        form = NotasIndividualesTutoradoForm()

    context = {
        'form': form,
        'tutoria_individual': tutoria_individual,
        'logged_in': logged_in,
        'rol': rol
    }
    return render(request, 'tutorado/tutoriaIndividual/crearNotaTutoriaIndividual.html', context)


def crear_tutoriaGrupal(request):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    if request.method == 'POST':
        form = TutoriaGrupalForm(request.POST)
        if form.is_valid():
            # Obtiene el tutor de la sesión
            tutor = Tutor.objects.get(
                numeroEmpleado=request.session['numero_empleado'])
            tutoria_grupal = form.save(commit=False)
            tutoria_grupal.idTutor = tutor
            tutoria_grupal.save()
            return redirect('menu')
    else:  # GET
        form = TutoriaGrupalForm()

    context = {'form': form, 'logged_in': logged_in, 'rol': rol}
    return render(request, 'tutor/tutoriaGrupal/crearTutoriaGrupal.html', context)


def detalle_tutoriaGrupal(request, tutoria_id):
    # Para proteger la ruta
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si NO estás logeado Y  no eres un Tutor or un Tutorado, redirige al inicio.
    if (not logged_in) and (rol != 'Tutor' or rol != 'Tutorado'):
        return redirect('inicio')

    else:
        # Obtener la instancia de TutoriaIndividual según el ID proporcionado
        tutoria_grupal = get_object_or_404(
            TutoriaGrupal, pk=tutoria_id)

        # Podemos obtener los detalles que queramos, como los anuncios del tutor
        # ...

        # Renderizar el template de detalle_tutoria.html con la instancia de tutoría individual
        context = {
            'tutoria_grupal': tutoria_grupal,
            'logged_in': logged_in,
            'rol': rol
        }
        return render(request, 'detalleTutoriaGrupal.html', context)
