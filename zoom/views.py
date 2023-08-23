import requests
from django.shortcuts import render, redirect
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
    access_token = 'eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6IjQ4ODkzNzEyLWNmNDMtNGFhZC04N2Q0LTRlMTAwZTA0YzMzNSJ9.eyJ2ZXIiOjksImF1aWQiOiJiOWU3N2EwOWQ0ZTBiMmRlYWY0NmMwZTAyNjE1MTdiNSIsImNvZGUiOiJZYldpM3BtUXhic2VqeGNwaDYzU0hTZGJzd3JfUjZvVWciLCJpc3MiOiJ6bTpjaWQ6ckFiemRCUW9TZmllYUZ5VVFmMmdCQSIsImdubyI6MCwidHlwZSI6MCwidGlkIjoyLCJhdWQiOiJodHRwczovL29hdXRoLnpvb20udXMiLCJ1aWQiOiJiRHFmVXJ3bFJtS2IwNHRJbDg2QmtnIiwibmJmIjoxNjkyODMzNTg0LCJleHAiOjE2OTI4MzcxODQsImlhdCI6MTY5MjgzMzU4NCwiYWlkIjoiMXNrUV9RUmVUZXFjbjJlRUJwdFV4ZyJ9.dPbWm42at57jLXd4EqRLyroi40BU7bF-GuOiyNm2L6p7nXRqLd3Ll0vZVDLf98PqETh8r0-Vczs676C7R9-v9A'
    scheduled_meetings = get_scheduled_meetings(access_token)

    return render(request, 'meetings.html', {'meetings': scheduled_meetings})
