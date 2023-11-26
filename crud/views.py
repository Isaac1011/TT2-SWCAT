from .forms import BitacoraIndividualTutorForm
from .models import BitacoraIndividualTutor, BitacoraGrupalTutor, AnunciosGrupalesTutor
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import TutorRegistroForm, TutorInicioSesionForm, TutoradoRegistroForm, TutoradoInicioSesionForm, TutoriaIndividualForm, BitacoraIndividualTutorForm, NotasIndividualesTutoradoForm, TutoriaGrupalForm, BitacoraGrupalTutorForm, AnunciosGrupalesTutorForm
from .models import Tutor, Tutorado, TutoriaIndividual, BitacoraIndividualTutor, NotasIndividualesTutorado, TutoriaGrupal, ListaTutoriaGrupal, VideoconferenciasIndividuales, VideoconferenciasGrupales
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_http_methods
import secrets
import string
from django.http import JsonResponse


# Create your views here.

# Esta función utiliza la decoración @require_http_methods(['GET']) para asegurarse de que solo responde a solicitudes GET.


@require_http_methods(['GET'])
def detalle_bitacora_individual(request, id_tutoria):

    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    template_name = 'detalleBitacoraIndividual.html'

    tutoria_individual = obtener_tutoria_individual(id_tutoria)
    notas_tutor = obtener_notas_tutor(tutoria_individual)

    context = {
        'tutoria_individual': tutoria_individual,
        'notas_tutor': notas_tutor,
        'logged_in': logged_in,
        'rol': rol
        # ... otras variables de contexto ...
    }

    return render(request, template_name, context)


def obtener_tutoria_individual(id_tutoria):
    # Aquí debes implementar la lógica para obtener la tutoría individual por su ID
    # Puedes utilizar el modelo BitacoraIndividualTutor y su correspondiente consulta en la base de datos
    bitacora_individual = BitacoraIndividualTutor.objects.get(
        idBitacoraIndividual=id_tutoria)
    return bitacora_individual.idTutoriaIndividual


def obtener_notas_tutor(tutoria_individual):
    # Aquí debes implementar la lógica para obtener las notas del tutor para una tutoría individual
    # Puedes utilizar el modelo BitacoraIndividualTutor y su correspondiente consulta en la base de datos
    notas_tutor = BitacoraIndividualTutor.objects.filter(
        idTutoriaIndividual=tutoria_individual)
    return notas_tutor


def detalle_bitacora_grupal(request, tutoria_id):

    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    tutoria_grupal = get_object_or_404(
        TutoriaGrupal, idTutoriaGrupal=tutoria_id)
    bitacoras_tutor = BitacoraGrupalTutor.objects.filter(
        idTutoriaGrupal=tutoria_grupal)

    context = {
        'tutoria_grupal': tutoria_grupal,
        'bitacoras_tutor': bitacoras_tutor,
        'logged_in': logged_in,
        'rol': rol
    }

    return render(request, 'detalleBitacoraGrupal.html', context)


def anuncios_grupales_tutor(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    tutoria_grupal = get_object_or_404(
        TutoriaGrupal, idTutoriaGrupal=tutoria_id)
    anuncios_grupales = AnunciosGrupalesTutor.objects.filter(
        idTutoriaGrupal=tutoria_grupal)

    context = {
        'tutoria_grupal': tutoria_grupal,
        'anuncios_grupales': anuncios_grupales,
        'logged_in': logged_in,
        'rol': rol
    }

    return render(request, 'anunciosGrupalesTutor.html', context)


def notas_tutorado_tutoria_individual(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutorado':
        return redirect('inicio')

    tutoria_individual = get_object_or_404(
        TutoriaIndividual, idTutoriaIndividual=tutoria_id)
    notas_tutorado = NotasIndividualesTutorado.objects.filter(
        idTutoriaIndividual=tutoria_individual)

    # Manejo del formulario para crear nuevas notas
    if request.method == 'POST':
        form = NotasIndividualesTutoradoForm(request.POST)
        if form.is_valid():
            nueva_nota = form.save(commit=False)
            nueva_nota.idTutoriaIndividual = tutoria_individual
            nueva_nota.save()
            # Puedes agregar un mensaje de éxito o redirigir a otra página si es necesario

    else:
        form = NotasIndividualesTutoradoForm()

    context = {
        'notas_tutorado': notas_tutorado,
        'tutoria_individual': tutoria_individual,
        'form': form,
        'logged_in': logged_in,
        'rol': rol
    }

    return render(request, 'notasIndividualesTutorado.html', context)


def hello_world(request):
    return HttpResponse("Hola mundo")


def inicio(request):
    # Obtiene el valor de 'logged_in' de la sesión, si no existe, se asigna False por defecto
    logged_in = request.session.get('logged_in', False)
    # Obtiene el valor de 'rol' de la sesión
    rol = request.session.get('rol')

    # Esto es para saber si está logeada, si es así, se muestra en pantalla
    context = {
        'logged_in': logged_in,
        'rol': rol
    }
    return render(request, 'inicio.html', context)


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
        tutorias_individuales = TutoriaIndividual.objects.filter(
            idTutorado=tutorado)
        # Recupera todas las tutorías grupales en las que está inscrito el Tutorado
        tutorias_grupales = ListaTutoriaGrupal.objects.filter(
            idTutorado=tutorado.idTutorado)

        # Renderiza la plantilla 'menuTutorado.html' con la información del usuario y las tutorías inscritas
        return render(request, 'tutorado/menuTutorado.html',
                      {'logged_in': logged_in,
                       'rol': rol,
                       'tutorias_individuales': tutorias_individuales,
                       'tutorias_grupales': tutorias_grupales}
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
                # password = Tutorado.objects.get(password=password)
                if check_password(password, tutorado.password):
                    # Inicio de sesión exitoso
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
                # tutorado.numTutoresAsignados += 1
                # tutorado.save()

                num = tutorado.numTutoresAsignados
                #  Actualizar el campo numTutoresAsignados incrementadndo en una unidad
                Tutorado.objects.filter(idTutorado=tutorado.idTutorado).update(
                    numTutoresAsignados=num + 1
                )

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

        # Obtener la VideoconferenciaIndividual según el ID proporcionado
        videoconferencia_individual = VideoconferenciasIndividuales.objects.filter(
            idTutoriaIndividual=tutoria_individual)

        # Renderizar el template de detalle_tutoria.html con la instancia de tutoría individual
        context = {
            'tutoria_individual': tutoria_individual,
            'notas_tutor': notas_tutor,
            'notas_tutorado': notas_tutorado,
            'videoconferencia_individual': videoconferencia_individual,
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


def generar_contrasena_aleatoria(longitud):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return contrasena


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

            # Genera una contraseña aleatoria de 20 caracteres
            password_grupo = generar_contrasena_aleatoria(20)
            tutoria_grupal.passwordGrupo = password_grupo

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
        # Obtener los Tutorados que pertenecen a esta tutoría grupal
        tutorados_pertenecientes = ListaTutoriaGrupal.objects.filter(
            idTutoriaGrupal=tutoria_grupal)
        # Obtener las bitácoras
        bitacoras_grupales = BitacoraGrupalTutor.objects.filter(
            idTutoriaGrupal=tutoria_grupal)
        # Obtener los anuncios de la tutoría grupal
        anuncios_grupales = AnunciosGrupalesTutor.objects.filter(
            idTutoriaGrupal=tutoria_grupal)
        # Podemos obtener los detalles que queramos, como los anuncios del tutor
        # ...

        # Obtener la VideoconferenciaIndividual según el ID proporcionado
        videoconferencia_grupal = VideoconferenciasGrupales.objects.filter(
            idTutoriaGrupal=tutoria_grupal)

        # Renderizar el template de detalle_tutoria.html con la instancia de tutoría individual
        context = {
            'tutoria_grupal': tutoria_grupal,
            'tutorados_pertenecientes': tutorados_pertenecientes,
            'bitacoras_grupales': bitacoras_grupales,
            'anuncios_grupales': anuncios_grupales,
            'videoconferencia_grupal': videoconferencia_grupal,
            'logged_in': logged_in,
            'rol': rol
        }
        return render(request, 'detalleTutoriaGrupal.html', context)


def buscar_tutoria_grupal(request):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')
    # Si no estás logeado o no eres un tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutorado':
        return redirect('inicio')

    tutorias_grupales = []  # Inicializa tutorias_grupales como una lista vacía

    if 'id_tutoria' in request.GET:
        id_tutoria = request.GET['id_tutoria']
        try:
            # Intenta convertir el ID a un número
            id_tutoria = int(id_tutoria)
            # Realiza la búsqueda en la base de datos por ID
            tutorias_grupales = TutoriaGrupal.objects.filter(
                idTutoriaGrupal=id_tutoria)
        except ValueError:
            # Captura la excepción si no se puede convertir a un número
            messages.error(
                request, 'Ingrese un número válido para la búsqueda por ID.')

    else:
        # Si no se proporciona un ID, muestra todas las tutorías disponibles
        tutorias_grupales = TutoriaGrupal.objects.all()

    # Renderizar el template de detalle_tutoria.html con la instancia de tutoría individual
    context = {
        'tutorias_grupales_disponibles': tutorias_grupales,
        'logged_in': logged_in,
        'rol': rol
    }
    return render(request, 'tutorado/tutoriaGrupal/inscribirseTutoriaGrupal.html', context)


def tutorias_grupales_disponibles(request):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutorado':
        return redirect('inicio')

    # Obtener todas las instancias de TutoriaGrupal que tengan cupo disponible
    tutorias_grupales_disponibles = TutoriaGrupal.objects.filter(
        cupoDisponible__gt=0)

    # Renderizar el template de detalle_tutoria.html con la instancia de tutoría individual
    context = {
        'tutorias_grupales_disponibles': tutorias_grupales_disponibles,
        'logged_in': logged_in,
        'rol': rol
    }
    return render(request, 'tutorado/tutoriaGrupal/inscribirseTutoriaGrupal.html', context)


def inscribirse_tutoria_grupal(request, tutoria_id):
    # Verificar que el tutorado esté autenticado y sea un tutorado
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    if not logged_in or rol != 'Tutorado':
        return redirect('inicio')

    # Obtener la tutoría grupal a la que se quiere inscribir el tutorado
    tutoria_grupal = get_object_or_404(
        TutoriaGrupal, idTutoriaGrupal=tutoria_id)

    # Verificar si hay cupo disponible en la tutoría grupal
    if tutoria_grupal.cupoDisponible <= 0:
        # Manejar el caso en que no haya cupo disponible
        messages.error(request, 'Tutoría Grupal llena')
    else:
        if request.method == 'POST':
            contrasena_grupo = request.POST.get('contrasena_grupo', '')
            # Verificar si la contraseña ingresada es correcta
            if contrasena_grupo == tutoria_grupal.passwordGrupo:
                # Crear una nueva instancia de ListaTutoriaGrupal para la inscripción
                tutorado_id = get_object_or_404(
                    Tutorado, boletaTutorado=request.session['boleta_tutorado'])
                # Verifica si el Tutorado tiene menos de 3 tutores asignados
                if tutorado_id.numTutoresAsignados >= 3:
                    # Muestra un mensaje de error si el Tutorado ya tiene 3 tutores asignados
                    messages.error(
                        request, 'El Tutorado ya está inscrito en 3 tutorías.')
                else:
                    # Verificar si el tutor ya está inscrito en la tutoría grupal
                    tutor_esta_inscrito = ListaTutoriaGrupal.objects.filter(
                        idTutoriaGrupal=tutoria_grupal,
                        idTutorado=tutorado_id
                    ).exists()
                    if tutor_esta_inscrito:
                        messages.error(
                            request, 'El Tutor ya está inscrito en esta Tutoría Grupal.')
                    else:
                        nueva_inscripcion = ListaTutoriaGrupal.objects.create(
                            idTutoriaGrupal=tutoria_grupal,
                            idTutorado=tutorado_id
                        )
                        # Reducir el cupo disponible en la tutoría grupal
                        tutoria_grupal.cupoDisponible -= 1
                        tutoria_grupal.save()
                        # Actualizar el campo numTutoresAsignados incrementando en una unidad
                        num = tutorado_id.numTutoresAsignados
                        Tutorado.objects.filter(boletaTutorado=request.session['boleta_tutorado']).update(
                            numTutoresAsignados=num + 1
                        )
                        return redirect('menu')
            else:
                # Muestra un mensaje de error si la contraseña ingresada es incorrecta
                messages.error(request, 'Contraseña incorrecta.')

    # Obtener todas las instancias de TutoriaGrupal que tengan cupo disponible
    tutorias_grupales_disponibles = TutoriaGrupal.objects.filter(
        cupoDisponible__gt=0)

    context = {
        'tutorias_grupales_disponibles': tutorias_grupales_disponibles,
        'logged_in': logged_in,
        'rol': rol
    }
    return render(request, 'tutorado/tutoriaGrupal/inscribirseTutoriaGrupal.html', context)


def bitacora_tutor_tutoriaGrupal(request, tutoria_id):
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
        tutoria_grupal = get_object_or_404(
            TutoriaGrupal, pk=tutoria_id)

    except TutoriaGrupal.DoesNotExist:
        # Manejo si la tutoría no existe
        messages.error(
            request, 'Tutoría no encontrada.')
        # return redirect('inicio')

    if request.method == 'POST':
        form = BitacoraGrupalTutorForm(request.POST)
        if form.is_valid():
            # Crea una nueva instancia de BitacoraGrupalTutor, pero aún no la guarda en la base de datos
            bitacora = form.save(commit=False)
            # Asigna la tutoría grupal
            bitacora.idTutoriaGrupal = tutoria_grupal
            bitacora.save()  # Ahora sí, guarda en la base de datos

            # Redirige a donde quieras después de registrar la nota
            # Cambia esto por la ruta adecuada
            return redirect('detalle_tutoriaGrupal', tutoria_id=tutoria_id)
    else:
        form = BitacoraIndividualTutorForm()

    context = {
        'form': form,
        'tutoria_grupal': tutoria_grupal,
        'logged_in': logged_in,
        'rol': rol
    }
    return render(request, 'tutor/tutoriaGrupal/crearBitacoraTutoriaGrupal.html', context)


def anuncio_tutor_tutoriaGrupal(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    # Con esto protejo la ruta menu/notaTutorIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de la tutoría individual según el ID proporcionado
        tutoria_grupal = get_object_or_404(
            TutoriaGrupal, pk=tutoria_id)
    except TutoriaGrupal.DoesNotExist:
        # Manejo si la tutoría no existe
        messages.error(
            request, 'Tutoría Grupal no encontrada.')
        # return redirect('inicio')

    if request.method == 'POST':
        form = AnunciosGrupalesTutorForm(request.POST)
        if form.is_valid():
            # Crear una instancia de NotasIndividualesTutorado pero no guardarla aún
            anuncio = form.save(commit=False)
            anuncio.idTutoriaGrupal = tutoria_grupal
            anuncio.save()
            return redirect('detalle_tutoriaGrupal', tutoria_id=tutoria_id)
    else:
        form = NotasIndividualesTutoradoForm()

    context = {
        'form': form,
        'tutoria_grupal': tutoria_grupal,
        'logged_in': logged_in,
        'rol': rol
    }
    return render(request, 'tutor/tutoriaGrupal/crearAnucionTutoriaGrupal.html', context)


def visor_imagenes(request):

    # Obtiene el valor de 'logged_in' de la sesión, si no existe, se asigna False por defecto
    logged_in = request.session.get('logged_in', False)
    # Obtiene el valor de 'rol' de la sesión
    rol = request.session.get('rol')

    # Esto es para saber si está logeada, si es así, se muestra en pantalla
    context = {
        'logged_in': logged_in,
        'rol': rol
    }
    return render(request, 'visor_imagenes.html', context)
