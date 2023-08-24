from django.shortcuts import render
import requests
import json
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import CrearReunionZoomForm
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
                    "type": 2,
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


def modificar_reunion(request, reunion_id):
    try:
        # Lógica para obtener los datos de la reunión en base al reunion_id
        reunion_data = {
            "topic": "Nombre de la reunión",
            "start_time": "2023-08-22T12:10:10Z",
            "duration": "3",
            # ... otros datos ...
        }

        return render(request, 'modificar_reunion.html', {'reunion_data': reunion_data})

    except Exception as e:
        error_message = f"An error occurred: {e}"
        return render(request, 'error.html', {'error_message': error_message})


# views.py

def guardar_modificacion_reunion(request, reunion_id):
    if request.method == 'POST':
        try:
            # Lógica para guardar los cambios en la reunión en base al reunion_id
            # Realiza la solicitud PUT a la API de Zoom para actualizar la reunión

            # Después de guardar los cambios, redirige a la lista de reuniones
            return redirect('zoom_meetings')

        except Exception as e:
            error_message = f"An error occurred: {e}"
            return render(request, 'error.html', {'error_message': error_message})
