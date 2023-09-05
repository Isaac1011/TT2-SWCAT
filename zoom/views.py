from django.shortcuts import render
import requests
import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import VideoconferenciasIndividualesForm, VideoconferenciasGrupalesForm
from crud.models import TutoriaIndividual, VideoconferenciasIndividuales, TutoriaGrupal, VideoconferenciasGrupales

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

    if request.method == 'POST':
        form = VideoconferenciasIndividualesForm(request.POST)
        if form.is_valid():
            try:

                # Obtener la instancia de TutoriaIndividual según el ID proporcionado
                tutoria_individual = get_object_or_404(
                    TutoriaIndividual, pk=tutoria_id)
                videoconferencia_individual = form.save(commit=False)
                videoconferencia_individual.idTutoriaIndividual = tutoria_individual

                # Datos de autenticación y formulario
                access_token = settings.TU_ACCESS_TOKEN  # Obtén el token de acceso previamente
                topic = form.cleaned_data['topic']
                start_time = form.cleaned_data['start_time']

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
                user_id = "bDqfUrwlRmKb04tIl86Bkg"
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

                print('AAAAAAAA')
                print(response_data)

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
                    error_message = f"Error al crear la reunión. Código de estado: {response.status_code}"
                    context = {
                        'error_message': error_message,
                        'logged_in': logged_in,
                        'rol': rol
                    }
                    return render(request, 'error.html', context)

            except requests.exceptions.RequestException as e:
                error_message = f"Error making a request: {e}"
                context = {'error_message': error_message,
                           'logged_in': logged_in,
                           'rol': rol}
                return render(request, 'error.html', context)
            except Exception as e:
                error_message = f"An error occurred: {e}"
                context = {'error_message': error_message,
                           'logged_in': logged_in,
                           'rol': rol}
                return render(request, 'error.html', context)
    else:
        form = VideoconferenciasIndividualesForm()

    context = {'form': form,
               'logged_in': logged_in,
               'rol': rol}
    return render(request, 'crearReunion.html', context)


def crear_reunion_grupal(request, tutoria_id):

    # Para proteger la ruta, verificamos si es un tutor y si tiene la sesión iniciada
    logged_in = request.session.get('logged_in', False)
    rol = request.session.get('rol')

    # Si no estás logeado o no eres un tutor, redirige al inicio.
    if not logged_in or rol != 'Tutor':
        return redirect('inicio')

    if request.method == 'POST':
        form = VideoconferenciasGrupalesForm(request.POST)
        if form.is_valid():
            try:

                # Obtener la instancia de TutoriaGrupal según el ID proporcionado
                tutoria_grupal = get_object_or_404(
                    TutoriaGrupal, pk=tutoria_id)
                videoconferencia_grupal = form.save(commit=False)
                videoconferencia_grupal.idTutoriaGrupal = tutoria_grupal

                # Datos de autenticación y formulario
                access_token = settings.TU_ACCESS_TOKEN  # Obtén el token de acceso previamente
                topic = form.cleaned_data['topic']
                start_time = form.cleaned_data['start_time']

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
                user_id = "bDqfUrwlRmKb04tIl86Bkg"
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

                print('AAAAAAAA')
                print(response_data)

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
                    error_message = f"Error al crear la reunión. Código de estado: {response.status_code}"
                    context = {
                        'error_message': error_message,
                        'logged_in': logged_in,
                        'rol': rol
                    }
                    return render(request, 'error.html', context)

            except requests.exceptions.RequestException as e:
                error_message = f"Error making a request: {e}"
                context = {'error_message': error_message,
                           'logged_in': logged_in,
                           'rol': rol}
                return render(request, 'error.html', context)
            except Exception as e:
                error_message = f"An error occurred: {e}"
                context = {'error_message': error_message,
                           'logged_in': logged_in,
                           'rol': rol}
                return render(request, 'error.html', context)
    else:
        form = VideoconferenciasIndividualesForm()

    context = {'form': form,
               'logged_in': logged_in,
               'rol': rol}
    return render(request, 'crearReunion.html', context)


def eliminar_reunion_individual(request, reunion_id):
    if request.method == 'POST':
        try:
            # Datos de autenticación
            access_token = settings.TU_ACCESS_TOKEN  # Obtén el token de acceso previamente

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


def eliminar_reunion_grupal(request, reunion_id):
    if request.method == 'POST':
        try:
            # Datos de autenticación
            access_token = settings.TU_ACCESS_TOKEN  # Obtén el token de acceso previamente

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

# No tengo permiso de modificar la reunión


# # Función para obtener los detalles de una reunión
# def obtener_datos_reunion(reunion_id, access_token):
#     # Realiza una solicitud GET a la API de Zoom para obtener los datos de la reunión
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#     }
#     reunion_url = f'https://api.zoom.us/v2/meetings/{reunion_id}'
#     response = requests.get(reunion_url, headers=headers)
#     reunion_data = response.json()
#     return reunion_data


# def modificar_reunion(request, reunion_id):
#     access_token = settings.TU_ACCESS_TOKEN

#     # Obtén los datos de la reunión
#     reunion_data = obtener_datos_reunion(reunion_id, access_token)

#     # Puebla el formulario con los datos de la reunión
#     form = ModificarReunionZoomForm(initial={
#         'topic': reunion_data['topic'],

#         'start_time': reunion_data['start_time'],
#         "duration": "3",
#         "settings": {
#                     "host_video": True,
#                     "participant_video": True,
#                     "join_before_host": True,
#                     "mute_upon_entry": "true",
#                     "watermark": "true",
#                     "    ": "voip",
#                     "auto_recording": "cloud"
#         }
#     })

#     return render(request, 'modificar_reunion.html', {'form': form,
#
#                                                   'reunion_id': reunion_id})
# LO SIGUIENTE IRÍA EN meetings.html
            # <!-- <a href="{% url 'modificar_reunion' reunion.id %}">Modificar</a> -->


# # Vista para guardar la modificación de la reunión


# def guardar_modificacion_reunion(request, reunion_id):

    # access_token = settings.TU_ACCESS_TOKEN
    # form = ModificarReunionZoomForm(request.POST)

    # if request.method == 'POST':

    #     form = ModificarReunionZoomForm(request.POST)

    #     if form.is_valid():
    #         # Obtén los datos modificados del formulario
    #         topic = form.cleaned_data['topic']
    #         start_time = form.cleaned_data['start_time']
    #         # Obtiene otros campos aquí

    #         # Formatear la fecha y hora en el formato requerido
    #         # formatted_start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    #         print("Start")
    #         print(start_time)

    #         # Realiza una solicitud PUT a la API de Zoom para actualizar los datos
    #         headers = {
    #             'Authorization': f'Bearer {access_token}',
    #             'Content-Type': 'application/json'
    #         }
    #         reunion_url = f'https://api.zoom.us/v2/meetings/{reunion_id}'
    #         payload = {
    #             'topic': topic,
    #             'start_time': start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
    #             "duration": "3",
    #             "settings": {
    #                 "host_video": True,
    #                 "participant_video": True,
    #                 "join_before_host": True,
    #                 "mute_upon_entry": "true",
    #                 "watermark": "true",
    #                 "audio": "voip",
    #                 "auto_recording": "cloud"
    #             }
    #         }
    #         response = requests.put(reunion_url, json=payload, headers=headers)

    #         print("AAAAAAAAAA")
    #         print(response.content)
    #         print(response.status_code)

    #         if response.status_code == 204:
    #             # La reunión se modificó exitosamente
    #             return redirect('zoom_meetings')
    #         else:
    #             # Hubo un error al modificar la reunión
    #             error_message = "Error al modificar la reunión"
    #             return render(request, 'error.html', {'error_message': error_message})

    # return render(request, 'modificar_reunion.html', {'form': form})


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
