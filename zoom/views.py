import requests
from django.shortcuts import render
from django.http import HttpResponse


def zoom_meetings(request):
    # Datos de autenticación
    client_id = 'rAbzdBQoSfieaFyUQf2gBA'
    client_secret = 'HUCoLXp4bqTYofGgIMTqeMSLYoq0BGDU'
    redirect_uri = 'https://oauth.pstmn.io/v1/callback'
    code = 'eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6ImYyMzc5NjBmLTg0ZjItNDQ3Mi1iY2M4LTc4OTMwMDJmZTgxOSJ9.eyJ2ZXIiOjksImF1aWQiOiJiOWU3N2EwOWQ0ZTBiMmRlYWY0NmMwZTAyNjE1MTdiNSIsImNvZGUiOiJZYldpM3BtUXhic2VqeGNwaDYzU0hTZGJzd3JfUjZvVWciLCJpc3MiOiJ6bTpjaWQ6ckFiemRCUW9TZmllYUZ5VVFmMmdCQSIsImdubyI6MCwidHlwZSI6MCwidGlkIjowLCJhdWQiOiJodHRwczovL29hdXRoLnpvb20udXMiLCJ1aWQiOiJiRHFmVXJ3bFJtS2IwNHRJbDg2QmtnIiwibmJmIjoxNjkyNjYyMDMyLCJleHAiOjE2OTI2NjU2MzIsImlhdCI6MTY5MjY2MjAzMiwiYWlkIjoiMXNrUV9RUmVUZXFjbjJlRUJwdFV4ZyJ9.T2I0ujwp8sESxOzAE3L4GANZsU9V2KXev8E47jpi-Run-cdNjmmgRMbQv2RZVEp1sgRzGqqps9cuCrm7fOgTFw'

    # Intercambiar el código por un token de acceso
    token_url = 'https://zoom.us/oauth/token'
    token_params = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
    }
    token_response = requests.post(token_url, auth=(
        client_id, client_secret), data=token_params)
    token_data = token_response.json()
    access_token = token_data.get('access_token')

    # Obtener la lista de reuniones programadas
    meetings_url = 'https://api.zoom.us/v2/users/me/meetings'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    meetings_response = requests.get(meetings_url, headers=headers)
    meetings_data = meetings_response.json()

    # Procesar y mostrar las reuniones en la plantilla
    meetings = meetings_data.get('meetings', [])
    print(meetings)
    return render(request, 'meetings.html', {'meetings': meetings})
