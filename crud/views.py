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
import pytz
from django.http import Http404
import re
from django.conf import settings
import requests
from zoom import views as Zoom

# Create your views here.

# Esta función utiliza la decoración @require_http_methods(['GET']) para asegurarse de que solo responde a solicitudes GET.


def eliminar_bitacora_tutoria_individual(request, id_tutor, id_bitacora):
    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de Tutorado según el ID proporcionado
        bitacora = BitacoraIndividualTutor.objects.get(
            idBitacoraIndividual=id_bitacora)
    except BitacoraIndividualTutor.DoesNotExist:
        messages.error(
            request, 'No fue posible encontrar la Bitácora Individual con el ID {}.'.format(id_bitacora))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        try:
            tutorSesion = Tutor.objects.get(
                numeroEmpleado=request.session['numero_empleado'])
        except Tutor.DoesNotExist:
            messages.error(
                request, 'No se encontró el Tutor de sesión')
            return redirect('menu')

        try:
            tutor = Tutor.objects.get(
                idTutor=id_tutor)
        except Tutor.DoesNotExist:
            messages.error(
                request, 'No se encontró el Tutor de parámetro')
            return redirect('menu')

        if tutor.idTutor == tutorSesion.idTutor:
            acceso = True

    if acceso:

        # Obtén la bitácora o devuelve un error 404 si no existe
        bitacora = get_object_or_404(
            BitacoraIndividualTutor, idBitacoraIndividual=id_bitacora)

        # Aquí puedes agregar lógica adicional, por ejemplo, verificar si el usuario tiene permisos para eliminar la bitácora.

        # Elimina la bitácora
        bitacora.delete()

        # Redirige a la página de detalle de bitácoras individuales o a donde lo necesites
        return redirect('detalle_bitacora_individual', id_tutoria=bitacora.idTutoriaIndividual.idTutoriaIndividual)

    else:
        messages.error(
            request, 'No tienes acceso a eliminar la Bitácora Individual con ID {}.'.format(id_bitacora))
        return redirect('menu')


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

    try:
        tutoria_individual = TutoriaIndividual.objects.get(
            idTutoriaIndividual=id_tutoria)
    except TutoriaIndividual.DoesNotExist:
        messages.error(
            request, 'La Tutoría Individual con el ID {} no fue encontrada.'.format(id_tutoria))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutoria_individual.idTutor.idTutor == tutor.idTutor:
            acceso = True

    if acceso:

        if tutoria_individual:
            try:
                notas_tutor = BitacoraIndividualTutor.objects.filter(
                    idTutoriaIndividual=tutoria_individual)
            except BitacoraIndividualTutor.DoesNotExist:
                messages.error(
                    request, 'Las Bitácoras Individuales de la Tutoría Individual con el ID {} no fueron encontradas.'.format(id_tutoria))
                return redirect('menu')

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
    else:
        messages.error(
            request, 'La Tutoría Individual con el ID {} no está a tu cargo.'.format(id_tutoria))
        return redirect('menu')


def eliminar_bitacora_grupal_tutoria(request, id_tutor, id_bitacora):
    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de Tutorado según el ID proporcionado
        bitacora = BitacoraGrupalTutor.objects.get(
            idBitacoraGrupalTutor=id_bitacora)
    except BitacoraGrupalTutor.DoesNotExist:
        messages.error(
            request, 'No fue posible encontrar la Bitácora Grupal con el ID {}.'.format(id_bitacora))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        try:
            tutorSesion = Tutor.objects.get(
                numeroEmpleado=request.session['numero_empleado'])
        except Tutor.DoesNotExist:
            messages.error(
                request, 'No se encontró el Tutor de sesión')
            return redirect('menu')

        try:
            tutor = Tutor.objects.get(
                idTutor=id_tutor)
        except Tutor.DoesNotExist:
            messages.error(
                request, 'No se encontró el Tutor de parámetro')
            return redirect('menu')

        if tutor.idTutor == tutorSesion.idTutor:
            acceso = True

    if acceso:

        # Obtén la bitácora grupal o devuelve un error 404 si no existe
        bitacora_grupal = get_object_or_404(
            BitacoraGrupalTutor, idBitacoraGrupalTutor=id_bitacora)

        # Aquí puedes agregar lógica adicional, por ejemplo, verificar si el usuario tiene permisos para eliminar la bitácora grupal.

        # Elimina la bitácora grupal
        bitacora_grupal.delete()

        # Redirige a la página de detalle de bitácoras grupales o a donde lo necesites
        return redirect('detalle_bitacora_grupal', tutoria_id=bitacora_grupal.idTutoriaGrupal.idTutoriaGrupal)

    else:
        messages.error(
            request, 'No tienes acceso a eliminar la Bitácora Grupal con ID {}.'.format(id_bitacora))
        return redirect('menu')


def detalle_bitacora_grupal(request, tutoria_id):

    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de TutoriaIndividual según el ID proporcionado
        tutoria_grupal = TutoriaGrupal.objects.get(
            idTutoriaGrupal=tutoria_id)
    except TutoriaGrupal.DoesNotExist:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no fue encontrada.'.format(tutoria_id))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutoria_grupal.idTutor.idTutor == tutor.idTutor:
            acceso = True

    if acceso:

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

    else:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no está a tu cargo.'.format(tutoria_id))
        return redirect('menu')


def eliminar_anuncio_grupal_tutoria(request, id_tutor, id_anuncio):
    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de Tutorado según el ID proporcionado
        anuncio = AnunciosGrupalesTutor.objects.get(
            idAnunciosGrupalesTutor=id_anuncio)
    except AnunciosGrupalesTutor.DoesNotExist:
        messages.error(
            request, 'No fue posible encontrar el Anuncio Grupal con el ID {}.'.format(id_anuncio))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        try:
            tutorSesion = Tutor.objects.get(
                numeroEmpleado=request.session['numero_empleado'])
        except Tutor.DoesNotExist:
            messages.error(
                request, 'No se encontró el Tutor de sesión')
            return redirect('menu')

        try:
            tutor = Tutor.objects.get(
                idTutor=id_tutor)
        except Tutor.DoesNotExist:
            messages.error(
                request, 'No se encontró el Tutor de parámetro')
            return redirect('menu')

        if tutor.idTutor == tutorSesion.idTutor:
            acceso = True

    if acceso:

        # Obtén el anuncio grupal o devuelve un error 404 si no existe
        anuncio_grupal = get_object_or_404(
            AnunciosGrupalesTutor, idAnunciosGrupalesTutor=id_anuncio)

        # Aquí puedes agregar lógica adicional, por ejemplo, verificar si el usuario tiene permisos para eliminar el anuncio grupal.

        # Elimina el anuncio grupal
        anuncio_grupal.delete()

        # Redirige a la página de anuncios grupales o a donde lo necesites
        return redirect('anuncios_grupales_tutor', tutoria_id=anuncio_grupal.idTutoriaGrupal.idTutoriaGrupal)

    else:
        messages.error(
            request, 'No tienes acceso a eliminar el Anuncio Grupal con ID {}.'.format(id_anuncio))
        return redirect('menu')


def anuncios_grupales_tutor(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de TutoriaIndividual según el ID proporcionado
        tutoria_grupal = TutoriaGrupal.objects.get(
            idTutoriaGrupal=tutoria_id)
    except TutoriaGrupal.DoesNotExist:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no fue encontrada.'.format(tutoria_id))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutoria_grupal.idTutor.idTutor == tutor.idTutor:
            acceso = True

    if acceso:

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

    else:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no está a tu cargo.'.format(tutoria_id))
        return redirect('menu')


def eliminar_nota_tutoria_individual(request, id_tutorado, id_nota):
    # Verifica si el usuario está logeado y es un tutorado
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutorado, redirige al inicio.
    if not logged_in or rol != 'Tutorado':
        return redirect('inicio')

    try:
        # Obtener la instancia de Tutorado según el ID proporcionado
        nota = NotasIndividualesTutorado.objects.get(
            idNotasIndividualesTutorado=id_nota)
    except NotasIndividualesTutorado.DoesNotExist:
        messages.error(
            request, 'No fue posible encontrar la nota con el ID {}.'.format(id_nota))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutorado':
        # Busco el tutor que tiene la sesión
        tutoradoSesion = Tutorado.objects.get(
            boletaTutorado=request.session['boleta_tutorado'])

        tutorado = Tutorado.objects.get(
            idTutorado=id_tutorado)

        if tutorado.idTutorado == tutoradoSesion.idTutorado:
            acceso = True

    if acceso:

        # Obtén la nota individual o devuelve un error 404 si no existe
        nota_individual = get_object_or_404(
            NotasIndividualesTutorado, idNotasIndividualesTutorado=id_nota)

        # Aquí puedes agregar lógica adicional, por ejemplo, verificar si el usuario tiene permisos para eliminar la nota individual.

        # Elimina la nota individual
        nota_individual.delete()

        # Redirige a la página de notas individuales o a donde lo necesites
        return redirect('notas_tutorado_tutoria_individual', tutoria_id=nota_individual.idTutoriaIndividual.idTutoriaIndividual)

    else:
        messages.error(
            request, 'No tienes acceso a eliminar la nota con ID {}.'.format(id_nota))
        return redirect('menu')


def notas_tutorado_tutoria_individual(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutorado':
        return redirect('inicio')

    try:
        # Obtener la instancia de Tutorado según el ID proporcionado
        tutoria_individual = TutoriaIndividual.objects.get(
            idTutoriaIndividual=tutoria_id)
    except TutoriaIndividual.DoesNotExist:
        messages.error(
            request, 'La Tutoría Individual con ID {} no fue encontrada.'.format(tutoria_id))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutorado':
        # Busco el tutor que tiene la sesión
        tutoradoSesion = Tutorado.objects.get(
            boletaTutorado=request.session['boleta_tutorado'])

        if tutoria_individual.idTutorado.idTutorado == tutoradoSesion.idTutorado:
            acceso = True

    if acceso:

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
            'rol': rol,
        }

        return render(request, 'notasIndividualesTutorado.html', context)

    else:
        messages.error(
            request, 'No estás inscrito en la Tutoría Individual con el ID {}.'.format(tutoria_id))
        return redirect('menu')


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
                    salon = form.cleaned_data['cubiculo']
                    if not cadena_alphanumeric(salon):
                        messages.error(
                            request, 'La sala no debe contener caracteres especiales.')
                    else:
                        numeroEmpleado = form.cleaned_data['numeroEmpleado']
                        if not numeroEmpleado.isdigit():
                            messages.error(
                                request, 'Ingrese un Número de Empleado válido.')
                        else:
                            if form.cleaned_data['acepta_terminos']:
                                nombre = form.cleaned_data['nombre']
                                # Llamamos la función desde otra app
                                user_id = Zoom.agregar_usuario_zoom(
                                    nombre, email)

                                if user_id:
                                    numero_empleado = form.cleaned_data['numeroEmpleado']
                                    tutor_instance = form.save(commit=False)
                                    tutor_instance.zoomUserID = user_id
                                    tutor_instance.save()
                                    # Inicio de sesión exitoso
                                    request.session['logged_in'] = True
                                    request.session['rol'] = 'Tutor'
                                    request.session['numero_empleado'] = numero_empleado
                                    # Agrega el mensaje
                                    # Agrega el mensaje
                                    messages.success(
                                        request, 'Se ha enviado un mensaje por parte de Zoom a su correo electrónico, favor de aceptar unirse a la cuenta principal de Zoom para tener acceso a crear videoconferencias')
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

    # Verificar si la dirección de correo electrónico termina con "@ipn.mx"
    if email.endswith("@ipn.mx"):
        return True

    try:
        # Validar la dirección de correo electrónico
        validate_email(email)
        return True
    except ValidationError:
        return False


def cadena_alphanumeric(cadena):
    # Utiliza una expresión regular para verificar si la cadena contiene solo caracteres alfanuméricos,
    # espacios, comas, dos puntos, puntos, guiones bajos y guiones medios.
    return bool(re.match("^[a-zA-Z0-9ñÑ ,:.\-_]+$", cadena))


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
                    boletaTutorado = form.cleaned_data['boletaTutorado']
                    if not boletaTutorado.isdigit():
                        messages.error(
                            request, 'Ingrese un Número de Boleta válido.')
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

    try:
        # Obtener la instancia de TutoriaIndividual según el ID proporcionado
        tutoria_individual = TutoriaIndividual.objects.get(
            idTutoriaIndividual=tutoria_id)
    except TutoriaIndividual.DoesNotExist:
        messages.error(
            request, 'La Tutoría Individual con el ID {} no fue encontrada.'.format(tutoria_id))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutoria_individual.idTutor.idTutor == tutor.idTutor:
            acceso = True

    if acceso:

        # Obtiene la tutoría individual correspondiente o devuelve un error 404 si no existe
        tutoria_individual = get_object_or_404(
            TutoriaIndividual, pk=tutoria_id)

        # Actualiza el valor del campo numTutoresAsignados en la tabla Tutorado
        Tutorado.objects.filter(pk=tutoria_individual.idTutorado.pk).update(
            numTutoresAsignados=F('numTutoresAsignados') - 1)

        # Elimina la tutoría individual
        tutoria_individual.delete()

        # Redirige a la página de inicio o cualquier otra página deseada
        return redirect('menu')

    else:
        messages.error(
            request, 'La Tutoría Individual con el ID {} no está a tu cargo.'.format(tutoria_id))
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

        try:
            # Obtener la instancia de TutoriaIndividual según el ID proporcionado
            tutoria_individual = get_object_or_404(
                TutoriaIndividual, pk=tutoria_id)

            # Verificar si el Tutor o Tutorado está inscrito a la tutoría individual que se pasa como parámetro
            acceso = False

            if rol == 'Tutor':
                tutor = Tutor.objects.get(
                    numeroEmpleado=request.session['numero_empleado'])

                if tutoria_individual.idTutor.idTutor == tutor.idTutor:
                    acceso = True

            elif rol == 'Tutorado':
                tutorado = Tutorado.objects.get(
                    boletaTutorado=request.session['boleta_tutorado'])

                if tutoria_individual.idTutorado.idTutorado == tutorado.idTutorado:
                    acceso = True

            if acceso:

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

            else:
                messages.error(
                    request, 'La Tutoría Individual con el ID {} no te pertenece.'.format(tutoria_id))
                return redirect('menu')

        except Http404:
            # Manejo del error cuando no se encuentra la tutoría
            messages.error(
                request, 'La Tutoría Individual con el ID {} no fue encontrada.'.format(tutoria_id))
            return redirect('menu')
            # Puedes redirigir al usuario a otra página, renderizar un template diferente, etc.


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
    except Http404:
        # Manejo del error cuando no se encuentra la tutoría
        messages.error(
            request, 'La Tutoría Individual con el ID {} no fue encontrada.'.format(tutoria_id))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutoria_individual.idTutor.idTutor == tutor.idTutor:
            acceso = True

    if acceso:

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
    else:
        messages.error(
            request, 'La Tutoría Individual con el ID {} no está a tu cargo.'.format(tutoria_id))
        return redirect('menu')


def nota_tutorado_tutoriaIndividual(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    # Con esto protejo la ruta menu/notaTutorIndividual/
    if not logged_in or rol != 'Tutorado':
        return redirect('inicio')

    try:
        # Obtener la instancia de TutoriaIndividual según el ID proporcionado
        tutoria_individual = get_object_or_404(
            TutoriaIndividual, pk=tutoria_id)
    except Http404:
        # Manejo del error cuando no se encuentra la tutoría
        messages.error(
            request, 'La Tutoría Individual con el ID {} no fue encontrada.'.format(tutoria_id))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutorado':
        # Busco el tutor que tiene la sesión
        tutorado = Tutorado.objects.get(
            boletaTutorado=request.session['boleta_tutorado'])

        if tutoria_individual.idTutorado.idTutorado == tutorado.idTutorado:
            acceso = True

    if acceso:

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

    else:
        messages.error(
            request, 'No estás inscrito en la Tutoría Individual con el ID {}.'.format(tutoria_id))
        return redirect('menu')


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
        try:
            # Obtener la instancia de TutoriaIndividual según el ID proporcionado
            tutoria_grupal = get_object_or_404(
                TutoriaGrupal, pk=tutoria_id)

            # Verificar si el Tutor o Tutorado está inscrito a la tutoría individual que se pasa como parámetro
            acceso = False

            if rol == 'Tutor':
                tutor = Tutor.objects.get(
                    numeroEmpleado=request.session['numero_empleado'])

                print(f'IDTutor {tutor.idTutor}')

                print(f'idTutoria {tutoria_grupal.idTutor.idTutor}')

                if tutoria_grupal.idTutor.idTutor == tutor.idTutor:
                    acceso = True

            elif rol == 'Tutorado':
                tutorado = Tutorado.objects.get(
                    boletaTutorado=request.session['boleta_tutorado'])

                try:
                    # Verificamos que el tutorado esté en la lista de inscritos de la tutoría grupal, si sí se encuentra esta consulta entonces sí tiene permitido ingresar a la tutoría
                    lista_tutoria_grupal = ListaTutoriaGrupal.objects.get(
                        idTutorado=tutorado.idTutorado, idTutoriaGrupal=tutoria_grupal.idTutoriaGrupal)
                    acceso = True
                except:
                    # Si no se encuentra, no tiene permitido
                    acceso = False

            if acceso:

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

            else:
                messages.error(
                    request, 'La Tutoría Grupal con el ID {} no te pertenece.'.format(tutoria_id))
                return redirect('menu')

        except Http404:
            # Manejo del error cuando no se encuentra la tutoría
            messages.error(
                request, 'La Tutoría Grupal con el ID {} no fue encontrada.'.format(tutoria_id))
            return redirect('menu')
            # Puedes redirigir al usuario a otra página, renderizar un template diferente, etc.


def buscar_tutorados_tutoria_grupal(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')
    # Si no estás logeado o no eres un tutor, redirige al inicio.
    # Con esto protejo la ruta menu/crearTutoriaIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de TutoriaGrupal según el ID proporcionado
        tutoria_grupal = TutoriaGrupal.objects.get(
            idTutoriaGrupal=tutoria_id)
    except TutoriaGrupal.DoesNotExist:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no fue encontrada.'.format(tutoria_id))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutoria_grupal.idTutor.idTutor == tutor.idTutor:
            acceso = True

    if acceso:

        # Lógica para obtener los tutorados específicos según el ID de la tutoría
        tutoria_grupal = get_object_or_404(TutoriaGrupal, pk=tutoria_id)
        tutorados_especificos = ListaTutoriaGrupal.objects.filter(
            idTutoriaGrupal=tutoria_grupal).select_related('idTutorado').order_by('idTutorado__apellidoPaterno')
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        context = {
            'tutoria_grupal': tutoria_grupal,
            'tutorados_especificos': tutorados_especificos,
            'tutor': tutor,
            'logged_in': logged_in,
            'rol': rol
        }

        return render(request, 'tutoradosTutoriaGrupal.html', context)

    else:
        messages.error(
            request, 'La Tutoría Grupals con el ID {} no está a tu cargo.'.format(tutoria_id))
        return redirect('menu')


def eliminar_tutorado_tutoria_grupal(request, tutorado_id, tutoria_id):
    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de TutoriaIndividual según el ID proporcionado
        tutoria_grupal = TutoriaGrupal.objects.get(
            idTutoriaGrupal=tutoria_id)
    except TutoriaGrupal.DoesNotExist:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no fue encontrada.'.format(tutoria_id))
        return redirect('menu')

    try:
        relacion_tutorado_tutoria = ListaTutoriaGrupal.objects.filter(
            idTutorado=tutorado_id, idTutoriaGrupal=tutoria_id)

        print(f"Holaaa {relacion_tutorado_tutoria}")

        if not relacion_tutorado_tutoria.exists():
            messages.error(
                request, 'El Tutorado con el ID {} no fue encontrado en la Tutoría Grupal con ID {}'.format(tutorado_id, tutoria_id))
            return redirect('menu')

    except ListaTutoriaGrupal.DoesNotExist as e:
        messages.error(
            request, f'{e}')
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutoria_grupal.idTutor.idTutor == tutor.idTutor:
            acceso = True

    if acceso:

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

    else:
        messages.error(
            request, 'No tienes permitido eliminar al Tutorado con ID {}.'.format(tutorado_id))
        return redirect('menu')


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

    try:
        # Obtener la tutoría grupal a la que se quiere inscribir el tutorado
        tutoria_grupal = TutoriaGrupal.objects.get(
            idTutoriaGrupal=tutoria_id)
    except TutoriaGrupal.DoesNotExist:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no fue encontrada.'.format(tutoria_id))
        return redirect('menu')

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

    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    # Con esto protejo la ruta menu/notaTutorIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de TutoriaIndividual según el ID proporcionado
        tutoria_grupal = TutoriaGrupal.objects.get(
            idTutoriaGrupal=tutoria_id)
    except TutoriaGrupal.DoesNotExist:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no fue encontrada.'.format(tutoria_id))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutoria_grupal.idTutor.idTutor == tutor.idTutor:
            acceso = True

    if acceso:

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

    else:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no está a tu cargo.'.format(tutoria_id))
        return redirect('menu')


def bitacora_tutor_tutoriaGrupal(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    # Con esto protejo la ruta menu/notaTutorIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de TutoriaIndividual según el ID proporcionado
        tutoria_grupal = TutoriaGrupal.objects.get(
            idTutoriaGrupal=tutoria_id)
    except TutoriaGrupal.DoesNotExist:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no fue encontrada.'.format(tutoria_id))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutoria_grupal.idTutor.idTutor == tutor.idTutor:
            acceso = True

    if acceso:

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

    else:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no está a tu cargo.'.format(tutoria_id))
        return redirect('menu')


def anuncio_tutor_tutoriaGrupal(request, tutoria_id):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    # Con esto protejo la ruta menu/notaTutorIndividual/
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de TutoriaIndividual según el ID proporcionado
        tutoria_grupal = TutoriaGrupal.objects.get(
            idTutoriaGrupal=tutoria_id)
    except TutoriaGrupal.DoesNotExist:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no fue encontrada.'.format(tutoria_id))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutoria_grupal.idTutor.idTutor == tutor.idTutor:
            acceso = True

    if acceso:

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

    else:
        messages.error(
            request, 'La Tutoría Grupal con el ID {} no está a tu cargo.'.format(tutoria_id))
        return redirect('menu')


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

    try:
        # Obtener la instancia de Tutor según el ID proporcionado
        tutor = Tutor.objects.get(
            idTutor=tutor_id)
    except Tutor.DoesNotExist:
        messages.error(
            request, 'El Tutor con el ID {} no fue encontrado.'.format(tutor_id))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutorSesion = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutor.idTutor == tutorSesion.idTutor:
            acceso = True

    if acceso:

        # Utilizamos filter en lugar de get para obtener el queryset
        queryset = Tutor.objects.filter(idTutor=tutor_id)

        # Si no se encuentra el tutor, se redirige a una página de error 404
        tutor = get_object_or_404(queryset)

        if request.method == 'POST':
            form = TutorForm(request.POST, instance=tutor)
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
                        salon = form.cleaned_data['cubiculo']
                        if not cadena_alphanumeric(salon):
                            messages.error(
                                request, 'La sala no debe contener caracteres especiales.')
                        else:
                            # Utilizamos update para actualizar directamente en la base de datos
                            queryset.update(**form.cleaned_data)
                            # Ajusta el nombre de la URL a la que quieres redirigir
                            return redirect('menu')

            else:
                # Agregar mensajes de error del formulario a messages
                for field, error_list in form.errors.items():
                    for error in error_list:
                        messages.error(
                            request, f'{field.capitalize()}: {error}')

        else:
            form = TutorForm(instance=tutor)

        context = {
            'form': form,
            'logged_in': logged_in,
            'rol': rol
        }
        return render(request, 'tutor/editarTutor.html', context)

    else:
        messages.error(
            request, 'El ID de Tutor que intentas acceder no te pertenece.'.format(tutor_id))
        return redirect('menu')


def editar_tutorado(request, tutorado_id):
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    if not logged_in or rol != 'Tutorado':
        return redirect('inicio')

    try:
        # Obtener la instancia de Tutorado según el ID proporcionado
        tutorado = Tutorado.objects.get(
            idTutorado=tutorado_id)
    except Tutorado.DoesNotExist:
        messages.error(
            request, 'El Tutorado con el ID {} no fue encontrado.'.format(tutorado_id))
        return redirect('menu')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutorado':
        # Busco el tutor que tiene la sesión
        tutoradoSesion = Tutorado.objects.get(
            boletaTutorado=request.session['boleta_tutorado'])

        if tutorado.idTutorado == tutoradoSesion.idTutorado:
            acceso = True

    if acceso:

        queryset = Tutorado.objects.filter(idTutorado=tutorado_id)

        # Obtener el tutorado
        tutorado = queryset.first()

        if request.method == 'POST':
            form = TutoradoForm(request.POST, instance=tutorado)
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
                        # Actualizar en la base de datos utilizando update
                        queryset.update(**form.cleaned_data)
                        return redirect('menu')

            else:
                # Agregar mensajes de error del formulario a messages
                for field, error_list in form.errors.items():
                    for error in error_list:
                        messages.error(
                            request, f'{field.capitalize()}: {error}')

        else:
            form = TutoradoForm(instance=tutorado)

        context = {
            'form': form,
            'logged_in': logged_in,
            'rol': rol
        }
        return render(request, 'tutorado/editarTutorado.html', context)

    else:
        messages.error(
            request, 'El ID de Tutorado que intentas acceder no te pertenece.'.format(tutorado_id))
        return redirect('menu')


def enviar_mensaje(request, tutor_id, tutorado_id):
    # Para proteger la ruta
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si NO estás logeado Y no eres un Tutor or un Tutorado, redirige al inicio.
    if (not logged_in) or (rol not in ['Tutor', 'Tutorado']):
        return redirect('inicio')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutor_id == tutor.idTutor:
            acceso = True

    elif rol == 'Tutorado':
        # Busco el tutorado que tiene la sesión
        tutorado = Tutorado.objects.get(
            boletaTutorado=request.session['boleta_tutorado'])

        if tutorado_id == tutorado.idTutorado:
            acceso = True

    if acceso:
        try:
            # Obtener instancias de Tutor y Tutorado
            tutor = get_object_or_404(Tutor, idTutor=tutor_id)
            tutorado = get_object_or_404(Tutorado, idTutorado=tutorado_id)

            # Verificar si ya existe un Chat entre el Tutor y el Tutorado
            chat, creado = Chat.objects.get_or_create(
                idTutor=tutor, idTutorado=tutorado)

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

                    # Mensajes vistos
                    if rol == 'Tutor':
                        chat.mensajes_no_leidos_tutorado += 1
                    elif rol == 'Tutorado':
                        chat.mensajes_no_leidos_tutor += 1

                    chat.save()

                    print(f"Enviar Tutor {chat.mensajes_no_leidos_tutor}")
                    print(
                        f"Enviar Tutorado {chat.mensajes_no_leidos_tutorado}")

                    context = {
                        'logged_in': logged_in,
                        'rol': rol,
                        'tutor': tutor,
                        'tutorado': tutorado,
                    }

                    # Redirige a la misma vista después de enviar el mensaje
                    return redirect('enviar_mensaje', tutor_id=tutor_id, tutorado_id=tutorado_id)

            # Obtener mensajes asociados al Chat
            # mensajes_existentes = Mensaje.objects.filter(idChat=chat)

            context = {
                'logged_in': logged_in,
                'rol': rol,
                'tutor': tutor,
                'tutorado': tutorado,
            }

            return render(request, 'mensaje.html', context)
        except Http404:
            # Manejo del error cuando no se encuentra la tutoría
            messages.error(
                request, 'Error al buscar el chat entre Tutor y Tutorado')
            return redirect('menu')

    else:
        messages.error(
            request, 'El chat al que intentas acceder no te pertenece')
        return redirect('menu')


def obtener_mensajes(request, tutor_id, tutorado_id):
    # Para proteger la ruta
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si NO estás logeado Y no eres un Tutor or un Tutorado, redirige al inicio.
    if (not logged_in) or (rol not in ['Tutor', 'Tutorado']):
        return redirect('inicio')

    acceso = False

    # Seguridad en los parámetros de la URL
    if rol == 'Tutor':
        # Busco el tutor que tiene la sesión
        tutor = Tutor.objects.get(
            numeroEmpleado=request.session['numero_empleado'])

        if tutor_id == tutor.idTutor:
            acceso = True

    elif rol == 'Tutorado':
        # Busco el tutorado que tiene la sesión
        tutorado = Tutorado.objects.get(
            boletaTutorado=request.session['boleta_tutorado'])

        if tutorado_id == tutorado.idTutorado:
            acceso = True

    if acceso:

        tutor = get_object_or_404(Tutor, idTutor=tutor_id)
        tutorado = get_object_or_404(Tutorado, idTutorado=tutorado_id)
        chat, creado = Chat.objects.get_or_create(
            idTutor=tutor, idTutorado=tutorado)

        # Mensajes leidos
        if rol == 'Tutor':
            chat.mensajes_no_leidos_tutor = 0
        elif rol == 'Tutorado':
            chat.mensajes_no_leidos_tutorado = 0

        chat.save()

        print(f"Carga Tutor {chat.mensajes_no_leidos_tutor}")
        print(f"Carga Tutorado {chat.mensajes_no_leidos_tutorado}")

        mensajes_no_leidos_tutor = chat.mensajes_no_leidos_tutor
        mensajes_no_leidos_tutorado = chat.mensajes_no_leidos_tutorado

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
                'mensajes_no_leidos_tutor': mensajes_no_leidos_tutor,
                'mensajes_no_leidos_tutorado': mensajes_no_leidos_tutorado,
            })

        return JsonResponse({'mensajes': mensajes_json})

    else:
        messages.error(
            request, 'El chat al que intentas acceder no te pertenece')
        return redirect('menu')
