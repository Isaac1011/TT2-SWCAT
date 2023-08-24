from django import forms


# Creo un formulario para que se puedan crear Reuniones

class CrearReunionZoomForm(forms.Form):
    topic = forms.CharField(max_length=80)
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))


class ModificarReunionZoomForm(forms.Form):
    topic = forms.CharField(max_length=80)
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    # Agrega otros campos necesarios
