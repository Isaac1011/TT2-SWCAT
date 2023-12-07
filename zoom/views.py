from django.shortcuts import render
import requests
import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import VideoconferenciasIndividualesForm, VideoconferenciasGrupalesForm
from crud.models import TutoriaIndividual, VideoconferenciasIndividuales, TutoriaGrupal, VideoconferenciasGrupales, Tutor, TokenZoom
from django.utils import timezone
from django.contrib import messages
import base64
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.http import JsonResponse
import pytz


import requests

# Color hexadecimal #2856FF

'''Para obtener mi USER_ID, hago una petición GET en Postman con:
https://api.zoom.us/v2/users/me
'''


def get_scheduled_meetings(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    user_id = "bDqfUrwlRmKb04tIl86Bkg"
    create_meeting_url = f'https://api.zoom.us/v2/users/{user_id}/meetings'
    # meetings_url = 'https://api.zoom.us/v2/users/me/meetings'

    response = requests.get(create_meeting_url, headers=headers)
    response_data = response.json()

    return response_data  # Retorna los datos de la reunión


def zoom_meetings(request):
    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    else:
        # Debes obtener el token aquí, por ejemplo, a través de OAuth 2.0
        access_token = settings.TU_ACCESS_TOKEN

        scheduled_meetings = get_scheduled_meetings(access_token)

        context = {'meetings': scheduled_meetings,
                   'logged_in': logged_in,
                   'rol': rol}
        return render(request, 'meetings.html', context)


def crear_reunion_individual(request, tutoria_id):

    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
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

        if request.method == 'POST':
            form = VideoconferenciasIndividualesForm(request.POST)
            tutor = Tutor.objects.get(
                numeroEmpleado=request.session['numero_empleado'])
            if form.is_valid():
                try:

                    # Obtener la instancia de TutoriaIndividual según el ID proporcionado
                    tutoria_individual = get_object_or_404(
                        TutoriaIndividual, pk=tutoria_id)
                    videoconferencia_individual = form.save(commit=False)
                    videoconferencia_individual.idTutoriaIndividual = tutoria_individual

                    # Verificamos si el access token ha expirado
                    token_expirado = verificar_token_expirado()
                    if token_expirado == True:
                        # Si ha expirado, entonces generamos uno nuevo
                        if generar_access_token() == False:
                            # Si no se generó correctamente lo anunciamos
                            messages.error(
                                request, 'Error al generar el Access Token, inténtelo de nuevo por favor')
                            return redirect('menu')

                    # Si el token no está expirado entonces continuamos
                    # access_token = settings.TU_ACCESS_TOKEN
                    # Tomamos el access token de la base de datos
                    ultimo_registro_token = TokenZoom.objects.latest(
                        'idTokenZoom')
                    access_token = ultimo_registro_token.accessToken
                    topic = form.cleaned_data['topic']
                    # start_time = form.cleaned_data['start_time']
                    # Configurar la fecha y hora antes de guardar el formulario
                    start_time = timezone.now()

                    # Datos de la nueva reunión
                    # Configuración de la información de la reunión
                    meeting_data = {
                        "topic": topic,  # Título de la reunión
                        "type": 2,  # Tipo de reunión (programada)
                        # Hora de inicio en formato ISO 8601
                        "start_time": start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "duration": "40",  # Duración de la reunión en minutos

                        # Configuración adicional de la reunión
                        "settings": {
                            "host_video": True,  # Anfitrión puede iniciar su video
                            "participant_video": True,  # Participantes pueden iniciar su video
                            "join_before_host": True,  # Los participantes pueden unirse antes del anfitrión
                            "mute_upon_entry": "true",  # Silenciar a los participantes al unirse
                            "watermark": "true",  # Agregar marca de agua a la grabación
                            "audio": "voip",  # Participantes se unen con audio a través de Internet
                            "auto_recording": "cloud"  # Grabación automática en la nube de Zoom
                        }
                    }

                    # URL para crear la reunión
                    # user_id = "bDqfUrwlRmKb04tIl86Bkg"
                    # Obtener el valor de zoomUserID desde la instancia de Tutorado
                    user_id = tutor.zoomUserID
                    create_meeting_url = f'https://api.zoom.us/v2/users/{user_id}/meetings'
                    # create_meeting_url = 'https://api.zoom.us/v2/users/me/meetings'

                    headers = {
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': 'application/json'
                    }

                    response = requests.post(
                        create_meeting_url, json=meeting_data, headers=headers)
                    # Estos son los datos de la reunión que se acaba de crear
                    response_data = response.json()

                    if response.status_code == 201:
                        # La reunión se creó correctamente
                        # Estos son los datos de la reunión que se acaba de crear
                        response_data = response.json()

                        # Guardamos en la base de datos

                        # Supongamos que el enlace de la reunión está en el campo 'join_url' de la respuesta
                        start_url = response_data.get('start_url', '')
                        created_at = response_data.get('created_at', '')
                        join_url = response_data.get('join_url', '')
                        # Supongamos que el código de la reunión está en el campo 'meeting_code' y la contraseña en 'meeting_password'
                        meeting_code = response_data.get('id', '')
                        meeting_password = response_data.get(
                            'password', '')

                        videoconferencia_individual.topic = topic
                        videoconferencia_individual.start_time = start_time
                        videoconferencia_individual.created_at = created_at
                        videoconferencia_individual.start_url = start_url
                        videoconferencia_individual.join_url = join_url
                        videoconferencia_individual.meeting_code = meeting_code
                        videoconferencia_individual.meeting_password = meeting_password
                        videoconferencia_individual.save()

                        # Retornamos exitosamente
                        return redirect('menu')

                    else:
                        # Hubo un error al crear la reunión
                        error_message = f"Error al crear la reunión. Debe editar su información para ingresar su Zoom User ID. Código de estado: {response.status_code}"
                        context = {
                            'error_message': error_message,
                            'logged_in': logged_in,
                            'rol': rol,
                            'tutor': tutor
                        }
                        return render(request, 'error.html', context)

                except requests.exceptions.RequestException as e:
                    error_message = f"Error making a request: {e}"
                    context = {'error_message': error_message,
                               'logged_in': logged_in,
                               'rol': rol,
                               'tutor': tutor}
                    return render(request, 'error.html', context)
                except Exception as e:
                    error_message = f"An error occurred: {e}"
                    context = {'error_message': error_message,
                               'logged_in': logged_in,
                               'rol': rol,
                               'tutor': tutor}
                    return render(request, 'error.html', context)
        else:
            form = VideoconferenciasIndividualesForm()
            tutor = Tutor.objects.get(
                numeroEmpleado=request.session['numero_empleado'])

        context = {'form': form,
                   'logged_in': logged_in,
                   'rol': rol,
                   'tutor': tutor}
        return render(request, 'crearReunion.html', context)

    else:
        messages.error(
            request, 'La Tutoría Individual con el ID {} no está a tu cargo.'.format(tutoria_id))
        return redirect('menu')


def crear_reunion_grupal(request, tutoria_id):

    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
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
            form = VideoconferenciasGrupalesForm(request.POST)
            tutor = Tutor.objects.get(
                numeroEmpleado=request.session['numero_empleado'])
            if form.is_valid():
                try:

                    # Obtener la instancia de TutoriaGrupal según el ID proporcionado
                    tutoria_grupal = get_object_or_404(
                        TutoriaGrupal, pk=tutoria_id)
                    videoconferencia_grupal = form.save(commit=False)
                    videoconferencia_grupal.idTutoriaGrupal = tutoria_grupal

                    # Verificamos si el access token ha expirado
                    token_expirado = verificar_token_expirado()
                    if token_expirado == True:
                        # Si ha expirado, entonces generamos uno nuevo
                        if generar_access_token() == False:
                            # Si no se generó correctamente lo anunciamos
                            messages.error(
                                request, 'Error al generar el Access Token, inténtelo de nuevo por favor')
                            return redirect('menu')

                    # Si el token no está expirado entonces continuamos
                    # access_token = settings.TU_ACCESS_TOKEN
                    # Tomamos el access token de la base de datos
                    ultimo_registro_token = TokenZoom.objects.latest(
                        'idTokenZoom')
                    access_token = ultimo_registro_token.accessToken

                    topic = form.cleaned_data['topic']
                    # start_time = form.cleaned_data['start_time']
                    # Configurar la fecha y hora antes de guardar el formulario
                    start_time = timezone.now()

                    # Datos de la nueva reunión
                    # Configuración de la información de la reunión
                    meeting_data = {
                        "topic": topic,  # Título de la reunión
                        "type": 2,  # Tipo de reunión (programada)
                        # Hora de inicio en formato ISO 8601
                        "start_time": start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        "duration": "40",  # Duración de la reunión en minutos

                        # Configuración adicional de la reunión
                        "settings": {
                            "host_video": True,  # Anfitrión puede iniciar su video
                            "participant_video": True,  # Participantes pueden iniciar su video
                            "join_before_host": True,  # Los participantes pueden unirse antes del anfitrión
                            "mute_upon_entry": "true",  # Silenciar a los participantes al unirse
                            "watermark": "true",  # Agregar marca de agua a la grabación
                            "audio": "voip",  # Participantes se unen con audio a través de Internet
                            "auto_recording": "cloud"  # Grabación automática en la nube de Zoom
                        }
                    }

                    # URL para crear la reunión
                    # user_id = "bDqfUrwlRmKb04tIl86Bkg"
                    # Obtener el valor de zoomUserID desde la instancia de Tutorado
                    user_id = tutor.zoomUserID
                    create_meeting_url = f'https://api.zoom.us/v2/users/{user_id}/meetings'
                    # create_meeting_url = 'https://api.zoom.us/v2/users/me/meetings'

                    headers = {
                        'Authorization': f'Bearer {access_token}',
                        'Content-Type': 'application/json'
                    }

                    response = requests.post(
                        create_meeting_url, json=meeting_data, headers=headers)
                    # Estos son los datos de la reunión que se acaba de crear
                    response_data = response.json()

                    if response.status_code == 201:
                        # La reunión se creó correctamente
                        # Estos son los datos de la reunión que se acaba de crear
                        response_data = response.json()

                        # Guardamos en la base de datos

                        # Supongamos que el enlace de la reunión está en el campo 'join_url' de la respuesta
                        start_url = response_data.get('start_url', '')
                        created_at = response_data.get('created_at', '')
                        join_url = response_data.get('join_url', '')
                        # Supongamos que el código de la reunión está en el campo 'meeting_code' y la contraseña en 'meeting_password'
                        meeting_code = response_data.get('id', '')
                        meeting_password = response_data.get('password', '')

                        videoconferencia_grupal.topic = topic
                        videoconferencia_grupal.start_time = start_time
                        videoconferencia_grupal.created_at = created_at
                        videoconferencia_grupal.start_url = start_url
                        videoconferencia_grupal.join_url = join_url
                        videoconferencia_grupal.meeting_code = meeting_code
                        videoconferencia_grupal.meeting_password = meeting_password
                        videoconferencia_grupal.save()

                        # Retornamos exitosamente
                        return redirect('menu')

                    else:
                        # Hubo un error al crear la reunión
                        error_message = f"Error al crear la reunión. Debe editar su información para ingresar su Zoom User ID. Código de estado: {response.status_code}"
                        context = {
                            'error_message': error_message,
                            'logged_in': logged_in,
                            'rol': rol,
                            'tutor': tutor
                        }
                        return render(request, 'error.html', context)

                except requests.exceptions.RequestException as e:
                    error_message = f"Error making a request: {e}"
                    context = {'error_message': error_message,
                               'logged_in': logged_in,
                               'rol': rol,
                               'tutor': tutor}
                    return render(request, 'error.html', context)
                except Exception as e:
                    error_message = f"An error occurred: {e}"
                    context = {'error_message': error_message,
                               'logged_in': logged_in,
                               'rol': rol,
                               'tutor': tutor}
                    return render(request, 'error.html', context)
        else:
            form = VideoconferenciasGrupalesForm()
            tutor = Tutor.objects.get(
                numeroEmpleado=request.session['numero_empleado'])

        context = {'form': form,
                   'logged_in': logged_in,
                   'rol': rol,
                   'tutor': tutor}
        return render(request, 'crearReunion.html', context)

    else:
        messages.error(
            request, 'La Tutoría Individual con el ID {} no está a tu cargo.'.format(tutoria_id))
        return redirect('menu')


def eliminar_reunion_individual(request, reunion_id, tutor_id):
    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de Tutorado según el ID proporcionado
        reunion = VideoconferenciasIndividuales.objects.get(
            meeting_code=reunion_id)
    except VideoconferenciasIndividuales.DoesNotExist:
        messages.error(
            request, 'No fue posible encontrar la Videoconferencia Individual con el ID {}.'.format(reunion_id))
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
                idTutor=tutor_id)
        except Tutor.DoesNotExist:
            messages.error(
                request, 'No se encontró el Tutor de parámetro')
            return redirect('menu')

        if tutor.idTutor == tutorSesion.idTutor:
            acceso = True

    if acceso:

        if request.method == 'POST':
            try:
                # Verificamos si el access token ha expirado
                token_expirado = verificar_token_expirado()
                if token_expirado == True:
                    # Si ha expirado, entonces generamos uno nuevo
                    if generar_access_token() == False:
                        # Si no se generó correctamente lo anunciamos
                        messages.error(
                            request, 'Error al generar el Access Token, inténtelo de nuevo por favor')
                        return redirect('menu')

                # Si el token no está expirado entonces continuamos
                # access_token = settings.TU_ACCESS_TOKEN
                # Tomamos el access token de la base de datos
                ultimo_registro_token = TokenZoom.objects.latest(
                    'idTokenZoom')
                access_token = ultimo_registro_token.accessToken

                # Datos de autenticación
                # access_token = settings.TU_ACCESS_TOKEN  # Obtén el token de acceso previamente

                # URL para eliminar la reunión
                delete_meeting_url = f'https://api.zoom.us/v2/meetings/{reunion_id}'

                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }

                response = requests.delete(delete_meeting_url, headers=headers)

                if response.status_code == 204:
                    # Eliminamos la videoconferencia de la DB
                    try:
                        # Busca el registro por el campo 'meeting_code'
                        videoconferencia = get_object_or_404(
                            VideoconferenciasIndividuales, meeting_code=reunion_id)

                        # Elimina el registro
                        videoconferencia.delete()

                        # Redirige de vuelta a la lista de reuniones
                        return redirect('menu')

                    except requests.exceptions.RequestException as e:
                        error_message = f"Error making a request: {e}"
                        return render(request, 'error.html', {'error_message': error_message})

                    except VideoconferenciasIndividuales.DoesNotExist:
                        error_message = f"No se encontró una videoconferencia con ese código: {e}"
                        return render(request, 'error.html', {'error_message': error_message})

            except requests.exceptions.RequestException as e:
                error_message = f"Error making a request: {e}"
                return render(request, 'error.html', {'error_message': error_message})
            except Exception as e:
                error_message = f"An error occurred: {e}"
                return render(request, 'error.html', {'error_message': error_message})

    else:
        messages.error(
            request, 'No tienes acceso a eliminar la Videoconferencia Individual.')
        return redirect('menu')


def eliminar_reunion_grupal(request, reunion_id, tutor_id):
    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    try:
        # Obtener la instancia de Tutorado según el ID proporcionado
        reunion = VideoconferenciasGrupales.objects.get(
            meeting_code=reunion_id)
    except VideoconferenciasGrupales.DoesNotExist:
        messages.error(
            request, 'No fue posible encontrar la Videoconferencia Grupal con el ID {}.'.format(reunion_id))
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
                idTutor=tutor_id)
        except Tutor.DoesNotExist:
            messages.error(
                request, 'No se encontró el Tutor de parámetro')
            return redirect('menu')

        if tutor.idTutor == tutorSesion.idTutor:
            acceso = True

    if acceso:

        if request.method == 'POST':
            try:
                # Datos de autenticación

                # Verificamos si el access token ha expirado
                token_expirado = verificar_token_expirado()
                if token_expirado == True:
                    # Si ha expirado, entonces generamos uno nuevo
                    if generar_access_token() == False:
                        # Si no se generó correctamente lo anunciamos
                        messages.error(
                            request, 'Error al generar el Access Token, inténtelo de nuevo por favor')
                        return redirect('menu')

                # Si el token no está expirado entonces continuamos
                # access_token = settings.TU_ACCESS_TOKEN
                # Tomamos el access token de la base de datos
                ultimo_registro_token = TokenZoom.objects.latest(
                    'idTokenZoom')
                access_token = ultimo_registro_token.accessToken
                # URL para eliminar la reunión
                delete_meeting_url = f'https://api.zoom.us/v2/meetings/{reunion_id}'

                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }

                response = requests.delete(delete_meeting_url, headers=headers)

                if response.status_code == 204:
                    # Eliminamos la videoconferencia de la DB
                    try:
                        # Busca el registro por el campo 'meeting_code'
                        videoconferencia = get_object_or_404(
                            VideoconferenciasGrupales, meeting_code=reunion_id)

                        # Elimina el registro
                        videoconferencia.delete()

                        # Redirige de vuelta a la lista de reuniones
                        return redirect('menu')

                    except requests.exceptions.RequestException as e:
                        error_message = f"Error making a request: {e}"
                        return render(request, 'error.html', {'error_message': error_message})

                    except VideoconferenciasIndividuales.DoesNotExist:
                        error_message = f"No se encontró una videoconferencia con ese código: {e}"
                        return render(request, 'error.html', {'error_message': error_message})

            except requests.exceptions.RequestException as e:
                error_message = f"Error making a request: {e}"
                return render(request, 'error.html', {'error_message': error_message})
            except Exception as e:
                error_message = f"An error occurred: {e}"
                return render(request, 'error.html', {'error_message': error_message})

    else:
        messages.error(
            request, 'No tienes acceso a eliminar la Videoconferencia Grupal.')
        return redirect('menu')

# No tengo permiso de modificar la reunión


def crear_reunion_instantanea(request):
    access_token = settings.TU_ACCESS_TOKEN  # Obtén el token de acceso

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Reemplaza con el ID del usuario para el que deseas crear la reunión
    user_id = "bDqfUrwlRmKb04tIl86Bkg"
    create_meeting_url = f'https://api.zoom.us/v2/users/{user_id}/meetings'
    payload = {
        "topic": "Reunión Instantánea",
        "type": 1  # Tipo de reunión: 1 para instantánea
    }

    response = requests.post(create_meeting_url, json=payload, headers=headers)
    response_data = response.json()

    join_url = response_data.get('join_url')
    print("Hola")
    print(join_url)

    return render(request, 'instant_meeting.html', {'join_url': join_url})


def obtener_user_id(request):

    # Verifica si el usuario está logeado y es un tutor
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un Tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    # Definir la URL de la API de Zoom
    url = "https://api.zoom.us/v2/users/me"

# Verificamos si el access token ha expirado4
    print("1")
    token_expirado = verificar_token_expirado()
    print("2")
    if token_expirado == True:
        print("3")
        # Si ha expirado, entonces generamos uno nuevo
        if generar_access_token() == False:
            print("4")
            # Si no se generó correctamente lo anunciamos
            messages.error(
                request, 'Error al generar el Access Token, inténtelo de nuevo por favor')
            return redirect('menu')

    # Si el token no está expirado entonces continuamos
    # access_token = settings.TU_ACCESS_TOKEN
    # Tomamos el access token de la base de datos
    print("5")
    ultimo_registro_token = TokenZoom.objects.latest('idTokenZoom')
    access_token = ultimo_registro_token.accessToken
    print("6")
    # access_token = settings.TU_ACCESS_TOKEN  # Obtén el token de acceso

    # Configurar los encabezados con el token de autorización
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Hacer la solicitud GET a la API de Zoom
    response = requests.get(url, headers=headers)

    # Verificar si la solicitud fue exitosa (código de respuesta 200)
    if response.status_code == 200:
        # Parsear el JSON de la respuesta
        data = response.json()

        # Obtener el valor del campo user_id
        user_id = data.get("id")

        context = {
            'user_id': user_id,
            'logged_in': logged_in,
            'rol': rol
        }

        # Enviar el user_id al template
        return render(request, 'idZoom.html', context)
    else:
        # Enviar un mensaje de error al template
        context = {
            'status_code': response.status_code,
            'error_message': response.text,
            'logged_in': logged_in,
            'rol': rol
        }
        return render(request, 'idZoom.html', context)

# Este es para pruebas


def refresh_access_token(request):
    # Utiliza el refresh token para obtener un nuevo token de acceso
    token_url = "https://zoom.us/oauth/token"
    client_id = settings.CLIENTE_ID
    # Reemplaza con tu secreto de cliente de Zoom
    client_secret = settings.CLIENTE_SECRET
    refresh_token = settings.REFRESH_ACCES_TOKEN
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        # Extrae toda la información de la respuesta y agrega created_at y expires_at
        data = response.json()
        data['created_at'] = datetime.now().isoformat()
        expires_in_seconds = data.get('expires_in', 0)
        data['expires_at'] = (
            datetime.now() + timedelta(seconds=expires_in_seconds)).isoformat()

        # Devuelve la respuesta completa como contexto
        return render(request, 'token_result.html', {'data': data})
    else:
        # Maneja cualquier error que pueda ocurrir al intentar obtener un nuevo token
        error_message = f'Error al actualizar el token de acceso: {response.text}'
        return render(request, 'error.html', {'error_message': error_message}, status=500)


def generar_access_token():
    # Utiliza el refresh token para obtener un nuevo token de acceso
    token_url = "https://zoom.us/oauth/token"
    client_id = settings.CLIENTE_ID
    client_secret = settings.CLIENTE_SECRET
    refresh_token = settings.REFRESH_ACCES_TOKEN
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        # Extrae toda la información de la respuesta y agrega created_at y expires_at
        data = response.json()
        data['created_at'] = datetime.now().isoformat()
        expires_in_seconds = data.get('expires_in', 0)
        data['expires_at'] = (
            datetime.now() + timedelta(seconds=expires_in_seconds)).isoformat()

        # Crea un nuevo registro en la base de datos utilizando el modelo TokenZoom
        nuevo_token = TokenZoom(
            accessToken=data['access_token'],
            tipoToken=data['token_type'],
            fechaCreado=data['created_at'],
            fechaExpira=data['expires_at']
        )
        nuevo_token.save()

        print("Access Token creado con éxito")

        return True
    else:
        # Manejo de errores si la respuesta no es 200
        print("Error al generar el Access Token")
        return False

# Si el token ha expirado regresa True


def verificar_token_expirado():
    try:
        # Consulta la base de datos para obtener el último registro
        ultimo_token = TokenZoom.objects.latest('idTokenZoom')

        # Obtiene la zona horaria de la Ciudad de México
        tz_mexico = pytz.timezone('America/Mexico_City')

        # Obtiene la fecha de expiración del token y la convierte a la zona horaria de México
        fecha_expira = ultimo_token.fechaExpira.replace(
            tzinfo=pytz.UTC).astimezone(tz_mexico)

        # Obtiene la fecha y hora actual en la zona horaria de México
        fecha_actual = datetime.now(tz_mexico)

        # Compara las fechas
        es_expirado = fecha_expira < fecha_actual

        # Aunque la fecha se guarda distinto en la base de datos, cuando hago la comparación sí funciona bien

        print(f"Hora token: {fecha_expira}")
        print(f"Hora actual: {fecha_actual}")

        print(f"¿Ha expirado? {es_expirado}")

        return es_expirado

        return es_expirado
    except TokenZoom.DoesNotExist:
        # Si la tabla está vacía le generamos un registro
        print("Hola1")
        if generar_access_token():
            print("Hola2")
            print(f"Primer token insertado en la base de datos")
        else:
            print("Hola3")
            print(f"Error al insertar el primero token en la base de datos")
