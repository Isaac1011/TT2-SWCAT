from django.shortcuts import render
import requests
import json
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import CrearReunionZoomForm, ModificarReunionZoomForm
from django.http import HttpResponse


import requests


def get_scheduled_meetings(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    meetings_url = 'https://api.zoom.us/v2/users/me/meetings'

    response = requests.get(meetings_url, headers=headers)
    response_data = response.json()

    return response_data  # Retorna los datos de la reunión


def zoom_meetings(request):
    # Debes obtener el token aquí, por ejemplo, a través de OAuth 2.0
    access_token = settings.TU_ACCESS_TOKEN

    scheduled_meetings = get_scheduled_meetings(access_token)

    return render(request, 'meetings.html', {'meetings': scheduled_meetings})


def crear_reunion(request):
    if request.method == 'POST':
        form = CrearReunionZoomForm(request.POST)
        if form.is_valid():
            try:
                # Datos de autenticación y formulario
                access_token = settings.TU_ACCESS_TOKEN  # Obtén el token de acceso previamente
                topic = form.cleaned_data['topic']
                start_time = form.cleaned_data['start_time']

                # Datos de la nueva reunión
                meeting_data = {
                    "topic": topic,
                    "type": 1,
                    "start_time": start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "duration": "3",
                    "settings": {
                        "host_video": True,
                        "participant_video": True,
                        "join_before_host": True,
                        "mute_upon_entry": "true",
                        "watermark": "true",
                        "audio": "voip",
                        "auto_recording": "cloud"
                    }
                }

                # URL para crear la reunión
                create_meeting_url = 'https://api.zoom.us/v2/users/me/meetings'

                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }

                response = requests.post(
                    create_meeting_url, json=meeting_data, headers=headers)
                # Estos son los datos de la reunión que se acaba de crear
                response_data = response.json()

                # return render(request, 'crearReunion.html', {'form': form, 'response_data': response_data})
                return redirect('zoom_meetings')

            except requests.exceptions.RequestException as e:
                error_message = f"Error making a request: {e}"
                return render(request, 'error.html', {'error_message': error_message})
            except Exception as e:
                error_message = f"An error occurred: {e}"
                return render(request, 'error.html', {'error_message': error_message})
    else:
        form = CrearReunionZoomForm()

    return render(request, 'crearReunion.html', {'form': form})


def eliminar_reunion(request, reunion_id):
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
                # Redirige de vuelta a la lista de reuniones
                return redirect('zoom_meetings')

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

    access_token = settings.TU_ACCESS_TOKEN
    form = ModificarReunionZoomForm(request.POST)

    if request.method == 'POST':

        form = ModificarReunionZoomForm(request.POST)

        if form.is_valid():
            # Obtén los datos modificados del formulario
            topic = form.cleaned_data['topic']
            start_time = form.cleaned_data['start_time']
            # Obtiene otros campos aquí

            # Formatear la fecha y hora en el formato requerido
            # formatted_start_time = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')

            print("Start")
            print(start_time)

            # Realiza una solicitud PUT a la API de Zoom para actualizar los datos
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            reunion_url = f'https://api.zoom.us/v2/meetings/{reunion_id}'
            payload = {
                'topic': topic,
                'start_time': start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "duration": "3",
                "settings": {
                    "host_video": True,
                    "participant_video": True,
                    "join_before_host": True,
                    "mute_upon_entry": "true",
                    "watermark": "true",
                    "audio": "voip",
                    "auto_recording": "cloud"
                }
            }
            response = requests.put(reunion_url, json=payload, headers=headers)

            print("AAAAAAAAAA")
            print(response.content)
            print(response.status_code)

            if response.status_code == 204:
                # La reunión se modificó exitosamente
                return redirect('zoom_meetings')
            else:
                # Hubo un error al modificar la reunión
                error_message = "Error al modificar la reunión"
                return render(request, 'error.html', {'error_message': error_message})

    return render(request, 'modificar_reunion.html', {'form': form})


def crear_reunion_instantanea(request):
    access_token = settings.TU_ACCESS_TOKEN  # Obtén el token de acceso

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    create_meeting_url = 'https://api.zoom.us/v2/users/me/meetings'
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
