from .forms import BitacoraIndividualTutorForm
from .models import BitacoraIndividualTutor, BitacoraGrupalTutor, AnunciosGrupalesTutor
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import TutorRegistroForm, TutorInicioSesionForm, TutoradoRegistroForm, TutoradoInicioSesionForm, TutoriaIndividualForm, BitacoraIndividualTutorForm, NotasIndividualesTutoradoForm, TutoriaGrupalForm, BitacoraGrupalTutorForm, AnunciosGrupalesTutorForm
from .models import Tutor, Tutorado, TutoriaIndividual, BitacoraIndividualTutor, NotasIndividualesTutorado, TutoriaGrupal, ListaTutoriaGrupal, VideoconferenciasIndividuales, VideoconferenciasGrupales, Chat, Mensaje
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_http_methods
import secrets
import string
from django.http import JsonResponse
from django.db import transaction
from django.db import models
from django.db.models import F
from .forms import TutorForm
from .models import Tutorado
from .forms import TutoradoForm
from django.utils import timezone
from datetime import datetime
import pytz
from django import forms


# Create your views here.

# Esta función utiliza la decoración @require_http_methods(['GET']) para asegurarse de que solo responde a solicitudes GET.


def eliminar_bitacora_tutoria_individual(request, id_bitacora):
    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    # Obtén la bitácora o devuelve un error 404 si no existe
    bitacora = get_object_or_404(
        BitacoraIndividualTutor, idBitacoraIndividual=id_bitacora)

    # Aquí puedes agregar lógica adicional, por ejemplo, verificar si el usuario tiene permisos para eliminar la bitácora.

    # Elimina la bitácora
    bitacora.delete()

    # Redirige a la página de detalle de bitácoras individuales o a donde lo necesites
    return redirect('detalle_bitacora_individual', id_tutoria=bitacora.idTutoriaIndividual.idTutoriaIndividual)


@require_http_methods(['GET'])
def detalle_bitacora_individual(request, id_tutoria):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    template_name = 'detalleBitacoraIndividual.html'

    tutoria_individual = obtener_tutoria_individual(id_tutoria)

    if tutoria_individual:
        notas_tutor = obtener_notas_tutor(tutoria_individual)

        context = {
            'tutoria_individual': tutoria_individual,
            'notas_tutor': notas_tutor,
            'logged_in': logged_in,
            'rol': rol
            # ... otras variables de contexto ...
        }

        return render(request, template_name, context)
    else:
        messages.error(request, 'Tutoría no encontrada.')
        return redirect('inicio')


def obtener_tutoria_individual(id_tutoria):
    try:
        # Obtener la instancia de TutoriaIndividual según el ID proporcionado
        tutoria_individual = TutoriaIndividual.objects.get(
            idTutoriaIndividual=id_tutoria)
        return tutoria_individual
    except TutoriaIndividual.DoesNotExist:
        return None


def obtener_notas_tutor(tutoria_individual):
    # Obtener las notas del tutor para una tutoría individual
    notas_tutor = BitacoraIndividualTutor.objects.filter(
        idTutoriaIndividual=tutoria_individual)
    return notas_tutor


def eliminar_bitacora_grupal_tutoria(request, id_bitacora):
    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    # Obtén la bitácora grupal o devuelve un error 404 si no existe
    bitacora_grupal = get_object_or_404(
        BitacoraGrupalTutor, idBitacoraGrupalTutor=id_bitacora)

    # Aquí puedes agregar lógica adicional, por ejemplo, verificar si el usuario tiene permisos para eliminar la bitácora grupal.

    # Elimina la bitácora grupal
    bitacora_grupal.delete()

    # Redirige a la página de detalle de bitácoras grupales o a donde lo necesites
    return redirect('detalle_bitacora_grupal', tutoria_id=bitacora_grupal.idTutoriaGrupal.idTutoriaGrupal)


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


def eliminar_anuncio_grupal_tutoria(request, id_anuncio):
    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    # Obtén el anuncio grupal o devuelve un error 404 si no existe
    anuncio_grupal = get_object_or_404(
        AnunciosGrupalesTutor, idAnunciosGrupalesTutor=id_anuncio)

    # Aquí puedes agregar lógica adicional, por ejemplo, verificar si el usuario tiene permisos para eliminar el anuncio grupal.

    # Elimina el anuncio grupal
    anuncio_grupal.delete()

    # Redirige a la página de anuncios grupales o a donde lo necesites
    return redirect('anuncios_grupales_tutor', tutoria_id=anuncio_grupal.idTutoriaGrupal.idTutoriaGrupal)


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


def eliminar_nota_tutoria_individual(request, id_nota):
    # Verifica si el usuario está logeado y es un tutorado
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutorado, redirige al inicio.
    if not logged_in or rol != 'Tutorado':
        return redirect('inicio')

    # Obtén la nota individual o devuelve un error 404 si no existe
    nota_individual = get_object_or_404(
        NotasIndividualesTutorado, idNotasIndividualesTutorado=id_nota)

    # Aquí puedes agregar lógica adicional, por ejemplo, verificar si el usuario tiene permisos para eliminar la nota individual.

    # Elimina la nota individual
    nota_individual.delete()

    # Redirige a la página de notas individuales o a donde lo necesites
    return redirect('notas_tutorado_tutoria_individual', tutoria_id=nota_individual.idTutoriaIndividual.idTutoriaIndividual)


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
                       'tutorias_grupales': tutorias_grupales,
                       'tutor': tutor}
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
                       'tutorias_grupales': tutorias_grupales,
                       'tutorado': tutorado}
                      )

    # Si el usuario no está iniciado sesión o su rol no coincide
    else:
        # Redirige al usuario a la vista 'inicio'
        return redirect('inicio')


def registro_tutor(request):
    if request.method == 'POST':
        form = TutorRegistroForm(request.POST)
        if form.is_valid():
            # Validar la estructura del email
            email = form.cleaned_data['email']
            if not email_valido(email):
                messages.error(request, 'Ingrese un email válido.')
            else:
                # Validar que el número de teléfono solo contenga números
                telefono = form.cleaned_data['telefono']
                if not telefono.isdigit():
                    messages.error(
                        request, 'Ingrese un número de teléfono válido.')
                else:
                    if form.cleaned_data['acepta_terminos']:
                        numero_empleado = form.cleaned_data['numeroEmpleado']
                        form.save()
                        # Inicio de sesión exitoso
                        request.session['logged_in'] = True
                        request.session['rol'] = 'Tutor'
                        request.session['numero_empleado'] = numero_empleado
                        return redirect('menu')
                    else:
                        messages.error(
                            request, 'Debe aceptar los términos y condiciones para registrarse.')
        else:
            # Agregar mensajes de error del formulario a messages
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'{field.capitalize()}: {error}')

    else:  # GET
        form = TutorRegistroForm()

    return render(request, 'tutor/registroTutor.html', {'form': form})


def email_valido(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def registro_tutorado(request):
    if request.method == 'POST':
        form = TutoradoRegistroForm(request.POST)
        if form.is_valid():
            # Validar la estructura del email
            email = form.cleaned_data['email']
            if not email_valido(email):
                messages.error(request, 'Ingrese un email válido.')
            else:
                # Validar que el número de teléfono solo contenga números
                telefono = form.cleaned_data['telefono']
                if not telefono.isdigit():
                    messages.error(
                        request, 'Ingrese un número de teléfono válido.')
                else:
                    if form.cleaned_data['acepta_terminos']:
                        boleta_tutorado = form.cleaned_data['boletaTutorado']
                        form.save()
                        # Inicio de sesión exitoso
                        request.session['logged_in'] = True
                        request.session['rol'] = 'Tutorado'
                        request.session['boleta_tutorado'] = boleta_tutorado
                        return redirect('menu')
                    else:
                        messages.error(
                            request, 'Debe aceptar los términos y condiciones para registrarse.')
        else:
            # Agregar mensajes de error del formulario a messages
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:  # GET
        form = TutoradoRegistroForm()

    return render(request, 'tutorado/registroTutorado.html', {'form': form})


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
                        request, 'Contraseña incorrecta. Inténtalo de nuevo.')
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
                else:
                    # Credenciales inválidas
                    messages.error(
                        request, 'Contraseña incorrecta. Inténtalo de nuevo.')

            except Tutorado.DoesNotExist:
                # Tutor no encontrado
                messages.error(request, 'Tutorado no encontrado.')

    else:
        form = TutoradoInicioSesionForm()

    return render(request, 'tutorado/inicioSesionTutorado.html', {'form': form})


def cerrar_sesion(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('inicio')


@transaction.atomic
def crear_tutoriaIndividual(request):
    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if request.method == 'POST':
        form = TutoriaIndividualForm(request.POST)
        if form.is_valid():
            boleta_tutorado = form.cleaned_data['boletaTutorado']
            nombre_tutoria_individual = form.cleaned_data['nombreTutoriaIndividual']

            try:
                tutorado = Tutorado.objects.get(boletaTutorado=boleta_tutorado)
            except Tutorado.DoesNotExist:
                messages.error(request, 'El tutorado no existe en el sistema.')
                context = {'form': form,
                           'logged_in': logged_in,
                           'rol': rol}
                return render(request, 'tutor/tutoriaIndividual/crearTutoriaIndividual.html', context)

            if tutorado.numTutoresAsignados >= 3:
                messages.error(
                    request, 'El tutorado ya está inscrito en 3 tutorías.')
                context = {'form': form,
                           'logged_in': logged_in,
                           'rol': rol}
                return render(request, 'tutor/tutoriaIndividual/crearTutoriaIndividual.html', context)

            tutor = Tutor.objects.get(
                numeroEmpleado=request.session['numero_empleado'])
            tutoria_individual = TutoriaIndividual(
                idTutor=tutor,
                idTutorado=tutorado,
                nombreTutoriaIndividual=nombre_tutoria_individual
            )
            tutoria_individual.save()

            Tutorado.objects.filter(boletaTutorado=boleta_tutorado).update(
                numTutoresAsignados=F('numTutoresAsignados') + 1)

            # messages.success(
            #     request, 'Tutoría individual creada exitosamente.')
            return redirect('menu')  # Cambiar por la ruta adecuada

    else:
        form = TutoriaIndividualForm()

    context = {'form': form, 'logged_in': logged_in, 'rol': rol}
    return render(request, 'tutor/tutoriaIndividual/crearTutoriaIndividual.html', context)


def eliminar_tutoria_individual(request, tutoria_id):
    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    # Obtiene la tutoría individual correspondiente o devuelve un error 404 si no existe
    tutoria_individual = get_object_or_404(TutoriaIndividual, pk=tutoria_id)

    # Actualiza el valor del campo numTutoresAsignados en la tabla Tutorado
    Tutorado.objects.filter(pk=tutoria_individual.idTutorado.pk).update(
        numTutoresAsignados=F('numTutoresAsignados') - 1)

    # Elimina la tutoría individual
    tutoria_individual.delete()

    # Redirige a la página de inicio o cualquier otra página deseada
    return redirect('menu')


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

        # Si es un Tutorado, lo buscamos
        if rol == 'Tutorado':
            tutorado = Tutorado.objects.get(
                boletaTutorado=request.session['boleta_tutorado'])
        else:
            tutorado = False
        # Podemos obtener los detalles que queramos, como los anuncios del tutor
        # ...

        # Obtener la VideoconferenciaIndividual según el ID proporcionado
        videoconferencia_grupal = VideoconferenciasGrupales.objects.filter(
            idTutoriaGrupal=tutoria_grupal)

        # Renderizar el template de detalle_tutoria.html con la instancia de tutoría individual
        context = {
            'tutorado': tutorado,
            'tutoria_grupal': tutoria_grupal,
            'tutorados_pertenecientes': tutorados_pertenecientes,
            'bitacoras_grupales': bitacoras_grupales,
            'anuncios_grupales': anuncios_grupales,
            'videoconferencia_grupal': videoconferencia_grupal,
            'logged_in': logged_in,
            'rol': rol
        }
        return render(request, 'detalleTutoriaGrupal.html', context)


def buscar_tutorados_tutoria_grupal(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')
    # Si no estás logeado o no eres un tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    # Lógica para obtener los tutorados específicos según el ID de la tutoría
    tutoria_grupal = get_object_or_404(TutoriaGrupal, pk=tutoria_id)
    tutorados_especificos = ListaTutoriaGrupal.objects.filter(
        idTutoriaGrupal=tutoria_grupal).select_related('idTutorado').order_by('idTutorado__apellidoPaterno')
    tutor = Tutor.objects.get(
        numeroEmpleado=request.session['numero_empleado'])

    context = {
        'tutorados_especificos': tutorados_especificos,
        'tutor': tutor,
        'logged_in': logged_in,
        'rol': rol
    }

    return render(request, 'tutoradosTutoriaGrupal.html', context)


def eliminar_tutorado_tutoria_grupal(request, tutorado_id):
    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    # Obtiene la relación ListaTutoriaGrupal correspondiente o devuelve un error 404 si no existe
    relacion_tutorado_tutoria = get_object_or_404(
        ListaTutoriaGrupal, idTutorado=tutorado_id)

    # Obtiene la tutoría grupal correspondiente
    tutoria_grupal = relacion_tutorado_tutoria.idTutoriaGrupal

    # Actualiza el valor del campo cupoDisponible en la tabla TutoriaGrupal
    TutoriaGrupal.objects.filter(pk=tutoria_grupal.pk).update(
        cupoDisponible=F('cupoDisponible') + 1)

    # Actualiza el valor del campo numTutoresAsignados en la tabla Tutorado
    Tutorado.objects.filter(pk=tutorado_id).update(
        numTutoresAsignados=F('numTutoresAsignados') - 1)

    # Elimina la relación ListaTutoriaGrupal
    relacion_tutorado_tutoria.delete()

    # Redirige a la página de tutorados específicos para la tutoría grupal
    return redirect('buscar_tutorados_tutoria_grupal', tutoria_id=tutoria_grupal.pk)


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
                            request, 'Ya estás inscrito en esta Tutoría Grupal.')
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


def eliminar_tutoria_grupal(request, tutoria_id):
    # Obtener la tutoría grupal
    tutoria_grupal = get_object_or_404(
        TutoriaGrupal, idTutoriaGrupal=tutoria_id)

    # Actualizar numTutoresAsignados del tutorado individual
    tutorados_inscritos = ListaTutoriaGrupal.objects.filter(
        idTutoriaGrupal=tutoria_grupal)
    for tutorado_inscrito in tutorados_inscritos:
        Tutorado.objects.filter(pk=tutorado_inscrito.idTutorado.idTutorado).update(
            numTutoresAsignados=F('numTutoresAsignados') - 1)

    # Eliminar tutoría grupal y tutorados inscritos
    tutorados_inscritos.delete()
    tutoria_grupal.delete()

    # Redirigir al menú u otra página de tu elección después de la eliminación
    return redirect('menu')  # Ajusta la ruta según tu configuración


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


def editar_tutor(request, tutor_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    # Con esto protejo la ruta menu/notaTutorIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    # Utilizamos filter en lugar de get para obtener el queryset
    queryset = Tutor.objects.filter(idTutor=tutor_id)

    # Si no se encuentra el tutor, se redirige a una página de error 404
    tutor = get_object_or_404(queryset)

    if request.method == 'POST':
        form = TutorForm(request.POST, instance=tutor)
        if form.is_valid():
            # Utilizamos update para actualizar directamente en la base de datos
            queryset.update(**form.cleaned_data)
            # Ajusta el nombre de la URL a la que quieres redirigir
            return redirect('menu')
    else:
        form = TutorForm(instance=tutor)

    context = {
        'form': form,
        'logged_in': logged_in,
        'rol': rol
    }
    return render(request, 'tutor/editarTutor.html', context)


def editar_tutorado(request, tutorado_id):
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    if not logged_in or rol != 'Tutorado':
        return redirect('inicio')

    queryset = Tutorado.objects.filter(idTutorado=tutorado_id)

    # Obtener el tutorado
    tutorado = queryset.first()

    if request.method == 'POST':
        form = TutoradoForm(request.POST, instance=tutorado)
        if form.is_valid():
            # Actualizar en la base de datos utilizando update
            queryset.update(**form.cleaned_data)
            return redirect('menu')
    else:
        form = TutoradoForm(instance=tutorado)

    context = {
        'form': form,
        'logged_in': logged_in,
        'rol': rol
    }
    return render(request, 'tutorado/editarTutorado.html', context)


def enviar_mensaje(request, tutor_id, tutorado_id, es_grupal):
    # Para proteger la ruta
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si NO estás logeado Y no eres un Tutor or un Tutorado, redirige al inicio.
    if (not logged_in) or (rol not in ['Tutor', 'Tutorado']):
        return redirect('inicio')

    # Obtener instancias de Tutor y Tutorado
    tutor = get_object_or_404(Tutor, idTutor=tutor_id)
    tutorado = get_object_or_404(Tutorado, idTutorado=tutorado_id)

    # Verificar si ya existe un Chat entre el Tutor y el Tutorado
    chat, creado = Chat.objects.get_or_create(
        idTutor=tutor, idTutorado=tutorado)

    # Convierte el parámetro a un valor booleano, para saber si estamos en una Tutoria Grupal o Individual
    es_grupal_bool = es_grupal.lower() == 'true'

    if es_grupal_bool:
        # Obtener el objeto ListaTutoriaGrupal que cumple con los criterios de búsqueda
        lista_tutoria_grupal = get_object_or_404(
            ListaTutoriaGrupal, idTutorado=tutorado, idTutoriaGrupal__idTutor=tutor)

        # Puedes acceder al idTutoriaGrupal resultante con lista_tutoria_grupal.idTutoriaGrupal
        id_tutoria_grupal = lista_tutoria_grupal.idTutoriaGrupal
        id_tutoria_individual = False

    else:
        id_tutoria_individual = get_object_or_404(
            TutoriaIndividual, idTutor=tutor, idTutorado=tutorado)
        id_tutoria_grupal = False

    # Si la solicitud es un POST, procesar el formulario
    if request.method == 'POST':
        contenido = request.POST.get('contenido', '')
        if contenido:
            # Crear y guardar un nuevo mensaje
            if rol == 'Tutor':
                tutorEnvia = True
            else:
                tutorEnvia = False
            mensaje = Mensaje.objects.create(
                idChat=chat, tutorEnvia=tutorEnvia, contenido=contenido, fecha_envio=timezone.now())

            # mensajes_existentes = Mensaje.objects.filter(idChat=chat)

            context = {
                'logged_in': logged_in,
                'rol': rol,
                'tutor': tutor,
                'tutorado': tutorado,
                # 'mensajes_existentes': mensajes_existentes,
                'es_grupal_bool': es_grupal_bool,
                'id_tutoria_individual': id_tutoria_individual,
                'id_tutoria_grupal': id_tutoria_grupal
            }

            # Redirige a la misma vista después de enviar el mensaje
            return redirect('enviar_mensaje', tutor_id=tutor_id, tutorado_id=tutorado_id, es_grupal=es_grupal_bool)

    # Obtener mensajes asociados al Chat
    # mensajes_existentes = Mensaje.objects.filter(idChat=chat)

    context = {
        'logged_in': logged_in,
        'rol': rol,
        'tutor': tutor,
        'tutorado': tutorado,
        # 'mensajes_existentes': mensajes_existentes,
        'es_grupal_bool': es_grupal_bool,
        'id_tutoria_individual': id_tutoria_individual,
        'id_tutoria_grupal': id_tutoria_grupal
    }

    return render(request, 'mensaje.html', context)


def obtener_mensajes(request, tutor_id, tutorado_id, es_grupal):
    # Para proteger la ruta
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si NO estás logeado Y no eres un Tutor or un Tutorado, redirige al inicio.
    if (not logged_in) or (rol not in ['Tutor', 'Tutorado']):
        return redirect('inicio')

    tutor = get_object_or_404(Tutor, idTutor=tutor_id)
    tutorado = get_object_or_404(Tutorado, idTutorado=tutorado_id)
    chat, creado = Chat.objects.get_or_create(
        idTutor=tutor, idTutorado=tutorado)
    mensajes_existentes = Mensaje.objects.filter(idChat=chat)

    mensajes_json = []
    for mensaje in mensajes_existentes:
        # Convertir la fecha y hora a la zona horaria de Ciudad de México
        fecha_envio_mexico = mensaje.fecha_envio.astimezone(
            pytz.timezone('America/Mexico_City'))

        mensajes_json.append({
            'contenido': mensaje.contenido,
            'tutorEnvia': mensaje.tutorEnvia,
            'fecha_envio': fecha_envio_mexico.strftime("%Y-%m-%d %H:%M:%S %Z"),
        })

    return JsonResponse({'mensajes': mensajes_json})
